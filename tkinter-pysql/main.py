import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from scipy import interpolate
import db


class FuelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Графики из базы данных")

        self.con = db.ConnectionDB(login='test', password='252825', database='test_alg')

        # поле для ввода даты/времени начала
        self.start_label = tk.Label(root, text="Дата/время начала (timestamp):")
        self.start_label.grid(row=0, column=0)
        self.start_entry = tk.Entry(root)
        self.start_entry.grid(row=0, column=1)

        # поле для ввода даты/времени конца
        self.end_label = tk.Label(root, text="Дата/время конца (timestamp):")
        self.end_label.grid(row=1, column=0)
        self.end_entry = tk.Entry(root)
        self.end_entry.grid(row=1, column=1)

        # поле для выбора id
        self.id_label = tk.Label(root, text="Выберите id:")
        self.id_label.grid(row=2, column=0)
        self.id_var = tk.StringVar()
        self.id_menu = tk.OptionMenu(root, self.id_var, "433427026902662", "433019520494099", "433100526928004")
        self.id_menu.grid(row=2, column=1)

        # кнопка для обновления всех id
        self.update_ids_button = tk.Button(root, text="Все id автомобилей", command=self.update_ids)
        self.update_ids_button.grid(row=3, column=0, columnspan=2)

        # кнопка для отображения графика топлива
        self.fuel_button = tk.Button(root, text="Остаток топлива в баке (график)", command=self.plot_fuel)
        self.fuel_button.grid(row=4, column=0, columnspan=2)

        # кнопка для отображения графика скорости
        self.speed_button = tk.Button(root, text="Скорость/время (график)", command=self.plot_speed)
        self.speed_button.grid(row=5, column=0, columnspan=2)

    def update_ids(self):
        # получаю все уникальные ID из базы данных и обновляю в выпадающем списке
        self.con.cursor.execute("SELECT DISTINCT terminal_id FROM messages")
        ids = [row[0] for row in self.con.cursor.fetchall()]
        self.id_var.set(ids[0])  # Устанавливаем первый id как дефолтный
        menu = self.id_menu["menu"]
        menu.delete(0, "end")
        for id in ids:
            menu.add_command(label=id, command=tk._setit(self.id_var, id))

    def plot_speed(self):
        # получаю данные из полей ввода
        start_time = int(self.start_entry.get())
        end_time = int(self.end_entry.get())
        id_car = self.id_var.get()

        # получаю данные скорости
        data = self.con.get_data_speed()

        x = []
        y = []
        for i in data:
            if start_time <= i['timestamp'] <= end_time and i['terminal_id'] == id_car:
                x.append(datetime.utcfromtimestamp(i['timestamp']).strftime('%H:%M:%S'))
                y.append(i['speed'])

        if x:
            plt.figure(figsize=(10, 5))
            plt.plot(x, y)
            plt.xlabel('Время')
            plt.ylabel('Скорость (км/ч)')
            plt.title(f"График скорости автомобиля {id_car}")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("Ошибка", "Данные не найдены для заданного интервала времени!")

    def plot_fuel(self):
        try:
            # получаю время начала и конца из полей ввода
            start_time = int(self.start_entry.get())
            end_time = int(self.end_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные значения для времени!")
            return

        id_car = self.id_var.get()

        # получаю данные из базы
        data = self.con.get_can_data()

        # извлекаю калибровочные данные для интерполяции
        calib_data = self.con.get_calib_data()
        x_calib = [i['input_value'] for i in calib_data['calibrating_data']]
        y_calib = [i['output_value'] for i in calib_data['calibrating_data']]
        calibrating = interpolate.interp1d(x_calib, y_calib, fill_value="extrapolate")

        x = []  # время
        y = []  # уровень топлива (литры)
        y2 = []  # оригинальные данные LLS_0
        fuel_changes = []  # для графика заправок и сливов
        prev_fuel = None  # предыдущее значение уровня топлива

        for i in data:
            # фильтрую данные по времени и ID
            if start_time <= i['timestamp'] <= end_time and i['terminal_id'] == id_car:
                # получаю данные LLS_0 из can_data
                if 'LLS_0' in i['can_data']:
                    fuel_level = i['can_data']['LLS_0']
                    x.append(datetime.utcfromtimestamp(i['timestamp']).strftime('%H:%M:%S'))
                    y2.append(fuel_level)  # оригинальные данные (не переведенные в литры)
                    liters = calibrating(fuel_level)
                    y.append(liters)  # перевожу в литры

                    # алгоритм заправок и сливов
                    if prev_fuel is not None:
                        if fuel_level - prev_fuel > 40:
                            fuel_changes.append((x[-1], liters, 'Заправка'))
                        elif fuel_level - prev_fuel < -40:
                            fuel_changes.append((x[-1], liters, 'Слив'))
                    prev_fuel = fuel_level

        if not x or not y:
            messagebox.showinfo("Ошибка", "Нет данных для выбранного временного интервала и ID.")
            return

        # построение графика с уровнем топлива
        plt.figure(figsize=(10, 5))
        plt.plot(x, y, label="Уровень топлива (литры)", color='blue')

        # добавляю заправки и сливы
        for change in fuel_changes:
            time, level, event = change
            plt.annotate(f'{event}: {level:.2f}', xy=(time, level), xytext=(time, level + 10),
                         arrowprops=dict(facecolor='red', arrowstyle='->'), fontsize=9)

        plt.xlabel('Время')
        plt.ylabel('Уровень топлива (л)')
        plt.title(f"График остатка топлива для автомобиля {id_car}")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# инициализация Tkinter
root = tk.Tk()
app = FuelApp(root)
root.mainloop()
