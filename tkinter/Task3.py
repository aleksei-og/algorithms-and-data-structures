import tkinter as tk

def fahrenheit_to_celsius():
    try:
        fahrenheit = float(fahrenheit_entry.get())  # получаю введённое значение
        celsius = (fahrenheit - 32) * 5 / 9  # формула для перевода
        celsius_label.config(text=f"{celsius:.2f} °C")  # обновляю метку с результатом
    except ValueError:
        celsius_label.config(text="Неверный ввод")  # если введено не число

# создаю основное окно
root = tk.Tk()
root.title("Перевод Фаренгейт в Цельсий")

# поле для ввода градусов по Фаренгейту
fahrenheit_entry = tk.Entry(root, font=("Arial", 20), width=10)
fahrenheit_entry.grid(row=0, column=0, padx=10, pady=20)

# кнопка "Стрелочка"
arrow_button = tk.Button(root, text="➡️", font=("Arial", 20), command=fahrenheit_to_celsius, width=5)
arrow_button.grid(row=0, column=1, padx=10, pady=20)

# метка для отображения результата в Цельсиях
celsius_label = tk.Label(root, text="0.00 °C", font=("Arial", 20), width=10)
celsius_label.grid(row=0, column=2, padx=10, pady=20)

root.mainloop()
