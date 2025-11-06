import psycopg2
from psycopg2._json import Json

class ConnectionDB:
    def __init__(self, login, password, database):
        self.connect = psycopg2.connect(
            user=login,
            password=password,
            database=database
        )

        self.cursor = self.connect.cursor()

    def get_data_speed(self):
        self.cursor.execute("SELECT terminal_id, timestamp, speed FROM messages WHERE timestamp > 1677877200 AND timestamp < 1677963540 ORDER BY timestamp")
        return [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in self.cursor.fetchall()]

    def get_can_data(self):
        self.cursor.execute("SELECT terminal_id, timestamp, can_data, speed FROM messages WHERE timestamp > 1677877200 AND timestamp < 1677963540 ORDER BY timestamp")
        return [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in self.cursor.fetchall()]

    def get_calib_data(self):
        self.cursor.execute(
            "SELECT calibrating_data FROM calibrating WHERE deviceid_port LIKE '433427026902051_%' LIMIT 1")
        return [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                self.cursor.fetchall()][0]

if __name__ == '__main__':
    con = ConnectionDB(login='test', password='252825', database='test_alg')
    get_speed = con.get_can_data()
    print(get_speed)
