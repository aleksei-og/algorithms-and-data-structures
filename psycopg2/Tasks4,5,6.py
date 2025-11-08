import psycopg2
import matplotlib.pyplot as plt

dbname = "flights_db"
user = "test"
password = "252825"
host = "localhost"
port = "5432"

try:
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # устанавливаю кодировку CP1251 для соединения
    connection.set_client_encoding('WIN1251')

    cursor = connection.cursor()

    # шаг 3: Получение данных из таблицы
    cursor.execute("SELECT x, y FROM coordinates;")
    rows = cursor.fetchall()
    print("\nПолученные данные из таблицы:")
    for row in rows:
        print(row)

    # шаг 4: Создание двух списков (x и y), заполненных данными из таблицы
    x_values = [row[0] for row in rows]
    y_values = [row[1] for row in rows]

    # шаг 5: Построение графика
    plt.figure(figsize=(8, 6))
    plt.scatter(x_values, y_values, color='blue', label='Data Points')  # Диаграмма рассеяния
    plt.title('График: x vs y')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()

except Exception as e:
    print(f"Ошибка при выполнении операции: {e}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Соединение с базой данных закрыто.")
