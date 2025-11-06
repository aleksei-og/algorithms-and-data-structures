import matplotlib.pyplot as plt
from datetime import datetime
import db

con = db.ConnectionDB(login='test', password='252825', database='test_alg')

get_speed = con.get_data_speed()

x = []  # время в часах
y = []  # скорость

speed_limit = 60

start_time = get_speed[0]['timestamp']

for i in get_speed:
    # преобразую timestamp в количество часов от начала наблюдения
    hours_from_start = (i['timestamp'] - start_time) / 3600  # преобразую в часы

    x.append(hours_from_start)
    y.append(i['speed'])

    # детектирую превышение скорости
    if i['speed'] > speed_limit:
        exceeded_by = i['speed'] - speed_limit
        timestamp = datetime.utcfromtimestamp(i['timestamp']).strftime('%Y.%m.%d %H:%M:%S')
        print(f"Превышение скорости! Время: {timestamp}, Скорость: {i['speed']} км/ч, Превышение на {exceeded_by} км/ч")

plt.figure(figsize=(10,6))
plt.plot(x, y, label='Скорость', color='b')
plt.axhline(y=speed_limit, color='r', linestyle='--', label=f'Лимит скорости: {speed_limit} км/ч')
plt.title('График скорости от времени')
plt.xlabel('Время (часы от начала)')
plt.ylabel('Скорость (км/ч)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
