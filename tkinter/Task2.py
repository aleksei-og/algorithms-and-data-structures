import tkinter as tk
from random import randint

def roll_dice():
    result = randint(1, 6)
    result_label.config(text=str(result))  # обновляю метку с результатом

# создаю основное окно
root = tk.Tk()
root.title("Бросок кубика")

# создаю кнопку "Бросить"
roll_button = tk.Button(root, text="Бросить", command=roll_dice, font=("Arial", 20), width=10)
roll_button.pack(pady=20)  # Кнопка будет сверху, с отступом по вертикали

# созданю метку для отображения результата
result_label = tk.Label(root, text="0", font=("Arial", 50), width=5)
result_label.pack(pady=20)  # Результат будет снизу с отступом по вертикали

root.mainloop()
