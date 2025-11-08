import psycopg2
from psycopg2 import sql

dbname = "flights_db"
user = "test"
password = "252825"
host = "localhost"
port = "5432"

try:
    # подключаюсь к PostgreSQL, но не указываю базу данных (по умолчанию подключаюсь к 'postgres')
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
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        print(f"База данных {dbname} успешно создана.")
    else:
        print(f"База данных {dbname} уже существует.")

    # закрываю временное соединение с базой данных postgres
    cursor.close()
    connection.close()

    # подключаюсь к только что созданной базе данных
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # устанавливаю кодировку CP1251 для соединения
    connection.set_client_encoding('WIN1251')

    # создаю курсор для выполнения операций
    cursor = connection.cursor()

    # шаг 1: Создание таблицы (если не существует)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS flights (
        flight_number VARCHAR(10),
        departure_airport VARCHAR(100),
        arrival_airport VARCHAR(100),
        departure_time TIME,
        status VARCHAR(20),
        airline VARCHAR(50)
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица создана или уже существует.")

    # шаг 2: Вставка данных
    insert_query = """
    INSERT INTO flights (flight_number, departure_airport, arrival_airport, departure_time, status, airline)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = [
        ('FL123', 'Москва (Шереметьево)', 'Санкт-Петербург (Пулково)', '12:30:00', 'Вовремя', 'Aeroflot'),
        ('FL124', 'Москва (Домодедово)', 'Екатеринбург (Кольцово)', '13:15:00', 'Задержка', 'Emirates'),
        ('FL125', 'Москва (Шереметьево)', 'Казань (Казань)', '14:00:00', 'Отменен', 'S7'),
        ('FL126', 'Санкт-Петербург (Пулково)', 'Москва (Шереметьево)', '15:45:00', 'Вовремя', 'Aeroflot'),
        ('FL127', 'Казань (Казань)', 'Москва (Шереметьево)', '16:10:00', 'Вовремя', 'S7'),
        ('FL128', 'Екатеринбург (Кольцово)', 'Москва (Домодедово)', '17:30:00', 'Задержка', 'Emirates'),
        ('FL129', 'Москва (Шереметьево)', 'Ташкент (Ташкент)', '18:00:00', 'Вовремя', 'Aeroflot'),
        ('FL130', 'Санкт-Петербург (Пулково)', 'Минск (Минск)', '19:00:00', 'Вовремя', 'S7'),
        ('FL131', 'Москва (Шереметьево)', 'Самара (Курумоч)', '20:10:00', 'Задержка', 'Emirates'),
        ('FL132', 'Екатеринбург (Кольцово)', 'Краснодар (Краснодар)', '21:20:00', 'Вовремя', 'S7')
    ]

    # вставка данных в таблицу
    cursor.executemany(insert_query, data)
    connection.commit()
    print("Данные успешно вставлены.")

    # шаг 3: Проверка данных
    cursor.execute("SELECT * FROM flights;")
    rows = cursor.fetchall()
    print("Данные в таблице:")
    for row in rows:
        print(row)

    # 2. вывести все самолеты, принадлежащие компании АЭРОФЛОТ
    cursor.execute("SELECT * FROM flights WHERE airline = 'Aeroflot';")
    aeroflot_planes = cursor.fetchall()
    print("\nСамолеты компании АЭРОФЛОТ:")
    for row in aeroflot_planes:
        print(row)

    # 3. вывести все самолеты, не принадлежащие компании АЭРОФЛОТ
    cursor.execute("SELECT * FROM flights WHERE airline != 'Aeroflot';")
    non_aeroflot_planes = cursor.fetchall()
    print("\nСамолеты, не принадлежащие компании АЭРОФЛОТ:")
    for row in non_aeroflot_planes:
        print(row)

    # 5. удалить все данные из таблицы рейсов самолетов
    cursor.execute("DELETE FROM flights;")
    connection.commit()
    print("\nВсе данные из таблицы 'flights' удалены.")

    # 7. изменить данные для всех самолетов, принадлежащих компании АЭРОФЛОТ на АЭРОФЛОТ 2
    cursor.execute("UPDATE flights SET airline = 'Aeroflot 2' WHERE airline = 'Aeroflot';")
    connection.commit()
    print("\nДанные для всех самолетов компании АЭРОФЛОТ были изменены на АЭРОФЛОТ 2.")

    # 8. удалить все данные о компании АЭРОФЛОТ
    cursor.execute("DELETE FROM flights WHERE airline = 'Aeroflot 2';")
    connection.commit()
    print("\nВсе данные о компании АЭРОФЛОТ удалены.")

except Exception as e:
    print(f"Ошибка при выполнении операции: {e}")

finally:
    # закрытие курсора и соединения
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Соединение с базой данных закрыто.")
