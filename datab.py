import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, tg_id, name):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`tg_id`, `name`) VALUES (?, ?)",
                                       (tg_id, name,))

    def user_exists(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `tg_id` = ?",
                                         (tg_id,)).fetchall()
            return bool(len(result))

    def get_name(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT name FROM `users` WHERE `tg_id` = ?",
                                         (tg_id,)).fetchall()
            for row in result:
                user = row[0]
            return user

    def get_regions(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `regions`").fetchall()
            regions = []
            for row in result:
                regions.append(row[0])
            return regions

    def get_cities(self, name):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM `{name}`").fetchall()
            cities = []
            for row in result:
                cities.append(row[0])
            return cities

    def get_hospitals(self, name):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM `{name}`").fetchall()
            hospitals = []
            for row in result:
                hospitals.append(row[0])
            return hospitals
