import tkinter as tk
import json


# функция для отправки данных в формате JSON
def submit_form():
    # Получение данных из полей ввода
    form_data = {
        "Имя": name_entry.get(),
        "Фамилия": surname_entry.get(),
        "Адрес 1": address1_entry.get(),
        "Адрес 2": address2_entry.get(),
        "Город": city_entry.get(),
        "Регион": region_entry.get(),
        "Почтовый индекс": postal_code_entry.get(),
        "Страна": country_entry.get()
    }

    # преобразование данных в формат JSON и вывод в консоль
    print(json.dumps(form_data, ensure_ascii=False, indent=4))


# функция для очистки всех полей ввода
def clear_form():
    name_entry.delete(0, tk.END)
    surname_entry.delete(0, tk.END)
    address1_entry.delete(0, tk.END)
    address2_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    region_entry.delete(0, tk.END)
    postal_code_entry.delete(0, tk.END)
    country_entry.delete(0, tk.END)


# создаю основное окно
root = tk.Tk()
root.title("Форма ввода данных")

# метки и поля ввода для каждого из данных
tk.Label(root, text="Имя:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
name_entry = tk.Entry(root, font=("Arial", 14), width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Фамилия:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
surname_entry = tk.Entry(root, font=("Arial", 14), width=30)
surname_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Адрес 1:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
address1_entry = tk.Entry(root, font=("Arial", 14), width=30)
address1_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Адрес 2:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
address2_entry = tk.Entry(root, font=("Arial", 14), width=30)
address2_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Город:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
city_entry = tk.Entry(root, font=("Arial", 14), width=30)
city_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Регион:").grid(row=5, column=0, sticky="e", padx=10, pady=5)
region_entry = tk.Entry(root, font=("Arial", 14), width=30)
region_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Почтовый индекс:").grid(row=6, column=0, sticky="e", padx=10, pady=5)
postal_code_entry = tk.Entry(root, font=("Arial", 14), width=30)
postal_code_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Страна:").grid(row=7, column=0, sticky="e", padx=10, pady=5)
country_entry = tk.Entry(root, font=("Arial", 14), width=30)
country_entry.grid(row=7, column=1, padx=10, pady=5)

# кнопки для очистки формы и отправки данных
clear_button = tk.Button(root, text="Очистить", font=("Arial", 14), command=clear_form, width=15)
clear_button.grid(row=8, column=0, padx=10, pady=20)

submit_button = tk.Button(root, text="Отправить", font=("Arial", 14), command=submit_form, width=15)
submit_button.grid(row=8, column=1, padx=10, pady=20)

root.mainloop()
