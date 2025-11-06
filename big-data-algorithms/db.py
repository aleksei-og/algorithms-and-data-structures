import psycopg2
# \copy messages from 'C:\Users\sugawara\Desktop\test.csv' delimiter ',' csv header;


class ConnectionDB:
    def __init__(self, login, password, database):
        self.connect = psycopg2.connect(
            user=login,
            password=password,
            database=database
        )

        self.cursor = self.connect.cursor()

    def get_data_speed(self):
        # 1677877200
        # 1677963540
        self.cursor.execute("select timestamp, speed from messages where terminal_id='433427026902662' and timestamp > 1677877200 and timestamp < 1677963540 order by timestamp")
        return [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in self.cursor.fetchall()]

