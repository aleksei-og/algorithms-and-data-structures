import psycopg2
import random

dbname = "flights_db"
user = "test"
password = "252825"
host = "localhost"
port = "5432"

try:
    # подключаюсь к PostgreSQL, но не указываю базу данных (по умолчанию подключаемся к 'postgres')
    connection = psycopg2.connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host,
        port=port
    )
    connection.autocommit = True  # устанавливаю автокоммит, чтобы можно было создавать базы данных

    cursor = connection.cursor()

    # проверяю, существует ли база данных
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}';")
    exists = cursor.fetchone()

    # если база данных не существует, создаю ее
    if not exists:
        print(f"База данных {dbname} не существует. Создаем базу данных...")
        cursor.execute(f"CREATE DATABASE {dbname};")
        print(f"База данных {dbname} успешно создана.")
    else:
        print(f"База данных {dbname} уже существует.")

    # закрываю временное соединение с базой данных postgres
    cursor.close()
    connection.close()

    # подключаюмь к только что созданной базе данных
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # устанавливаю кодировку CP1251 для соединения
    connection.set_client_encoding('WIN1251')

    # создание курсора для выполнения операций
    cursor = connection.cursor()

    # шаг 1: Создание таблицы с полями x и y
    create_table_query = """
    CREATE TABLE IF NOT EXISTS coordinates (
        x INTEGER,
        y INTEGER
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица 'coordinates' успешно создана.")

    # шаг 2: Заполнение таблицы сгенерированными данными (минимум 30 записей)
    insert_query = "INSERT INTO coordinates (x, y) VALUES (%s, %s)"
    data = [(random.randint(1, 100), random.randint(1, 100)) for _ in range(30)]  # Генерация 30 случайных записей
    cursor.executemany(insert_query, data)
    connection.commit()
    print("Таблица успешно заполнена данными.")

except Exception as e:
    print(f"Ошибка при выполнении операции: {e}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Соединение с базой данных закрыто.")
