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
                regions.append(row[1])
            return regions

    def get_cities(self, name):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM `{name}`").fetchall()
            cities = []
            for row in result:
                cities.append(row[1])
            return cities

    def get_hospitals(self, name):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM `{name}`").fetchall()
            hospitals = []
            for row in result:
                hospitals.append(row[1])
            return hospitals

    def get_info(self, city, name):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM `{city}` WHERE `name` = ?", (name,)).fetchall()
            for row in result:
                res = row
            return res

    def set_city(self, city, tg_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `city` = ? WHERE `tg_id` = ?",
                                       (city, tg_id,))

    def get_city(self, tg_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT `city` FROM `users` WHERE `tg_id` == {tg_id}").fetchall()
            for row in result:
                answer = row[0]
            return answer

    def get_photo(self, tg_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT `photo` FROM `users` WHERE `tg_id` == {tg_id}").fetchall()
            for row in result:
                ans = row[0]
            return ans

    def set_photo(self, photo, tg_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `photo` = ? WHERE `tg_id` = ?",
                                       (photo, tg_id,))

    def get_docs(self, hospital):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `{hospital}`").fetchall()

    def get_doc(self, hospital, who):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `{hospital}` WHERE `who` = ?", (who,)).fetchall()

    def get_from_name(self, hospital, name):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `{hospital}` WHERE `name` = ?", (name,)).fetchall()

    def get_admin_name(self):
        with self.connection:
            result = self.cursor.execute(f"SELECT `name` FROM `admin`").fetchall()
            for row in result:
                name = row[0]
            return name

    def get_admin_password(self):
        with self.connection:
            result = self.cursor.execute(f"SELECT `pass` FROM `admin`").fetchall()
            for row in result:
                password = row[0]
            return password

    def delete_user(self, id):
        with self.connection:
            return self.cursor.execute(f"DELETE FROM `users` WHERE `tg_id` = {id}")

    def create_obl(self, name):
        with self.connection:
            self.cursor.execute(f"CREATE TABLE [{name}] (id INTEGER PRIMARY KEY UNIQUE NOT NULL, name TEXT);")
            self.cursor.execute(f"INSERT INTO `regions` (`name`) VALUES (?)", (name,))
            self.connection.commit()

    def check(self, name, flag=False):
        with self.connection:
            if flag:
                result = self.cursor.execute(
                    f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name[:14]}';").fetchall()
            else:
                result = self.cursor.execute(
                    f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}';").fetchall()
            return bool(len(result))

    def create_gor(self, name):
        with self.connection:
            return self.cursor.execute(
                f"CREATE TABLE {name} (id INTEGER PRIMARY KEY UNIQUE NOT NULL, name TEXT, address TEXT, number TEXT);")

    def add_gor(self, name, obl):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `{obl}` (`name`) VALUES (?)", (name,))

    def create_hospital(self, name):
        with self.connection:
            return self.cursor.execute(
                f"CREATE TABLE [{name[:14]}] (id INTEGER PRIMARY KEY UNIQUE NOT NULL, name TEXT, who TEXT, cabinet INTEGER);")

    def add_hos(self, name, gor, adr, num):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `{gor}` (`name`, `address`, `number`) VALUES (?, ?, ?)",
                                       (name, adr, num))

    def add_doc(self, name, who, hos, cab):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `{hos[:14]}` (`name`, `who`, `cabinet`) VALUES (?, ?, ?)",
                                       (name, who, cab))

    def del_doc(self, name, hos):
        with self.connection:
            return self.cursor.execute(f"DELETE FROM `{hos[:14]}` WHERE `name` = ?", (name,))
