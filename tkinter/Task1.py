import tkinter as tk

def increment():
    counter.set(counter.get() + 1)

def decrement():
    counter.set(counter.get() - 1)

# cоздаю основное окно
root = tk.Tk()
root.title("Счётчик")

# создаю переменную для хранения значения счётчика
counter = tk.IntVar()
counter.set(0)

# Создаю кнопку "+" для увеличения счётчика
plus_button = tk.Button(root, text="+", command=increment, font=("Arial", 20), width=5)
plus_button.grid(row=0, column=2)

# созданю кнопку "-" для уменьшения счётчика
minus_button = tk.Button(root, text="-", command=decrement, font=("Arial", 20), width=5)
minus_button.grid(row=0, column=0)

# создание метку для отображения значения счётчика
counter_label = tk.Label(root, textvariable=counter, font=("Arial", 20), width=5)
counter_label.grid(row=0, column=1)

root.mainloop()
