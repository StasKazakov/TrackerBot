import sqlite3


class Database:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, name_tg):
        with self.connection:
            result = self.cursor.execute("SELECT user_id FROM user_lang WHERE user_id = ?", (user_id,)).fetchall()
            if bool(len(result)) == False:
                return self.connection.execute("INSERT INTO user_lang (user_id, name_tg) VALUES (?,?)", (user_id, name_tg ))
            else:
                pass

    def save_language(self, language, user_id):  # Saving chose language to database
        with self.connection:
            return self.connection.execute("UPDATE user_lang  SET user_language = ? WHERE user_id = ?", (language, user_id ))

    def check_language(self, user_id):  # Function will check ordered language
        with self.connection:
            res = self.cursor.execute("SELECT user_language FROM user_lang WHERE user_id = ?", (user_id,)).fetchone()
            return ''.join(res)

    def save_link(self, user_id, root_link, track_link):
        # This function is not complete, will change in future commits
        with self.connection:
            return self.cursor.execute("INSERT INTO keys (user_id, root_link, track_link) VALUES (?,?,?)", (user_id, root_link, track_link))
    
    def save_event(self, user_id, root_link, track_link, data_time):
        with self.connection:
            return self.cursor.execute("INSERT INTO Events (user_id, root_link, track_link, data_time) VALUES (?,?,?)", (user_id, root_link, track_link, data_time))