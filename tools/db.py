import pymysql

class Database:
    
    def __init__ (self, param_host: str, param_user: str, param_password: str, param_database: str) -> None:
        self.connection = pymysql.connect(host=param_host,
                            user= param_user,
                            password= param_password,
                            database= param_database,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        
        
        
    def add_user(self, user_id: int, tg_name: str) -> None:
        with self.connection.cursor() as cursor:
                sql_request = "SELECT user_id FROM user_lang WHERE user_id = %s" 
                cursor.execute(sql_request, (user_id,))
                result = cursor.fetchall()
                if bool(len(result)) == False:
                    sql_formula = "INSERT INTO user_lang (user_id, tg_name) VALUES (%s, %s)"
                    cursor.execute(sql_formula, (user_id, tg_name))
                    self.connection.commit()
                else:
                    pass
            
    
    def save_language(self, language: str, user_id: int) -> None:
        with self.connection.cursor() as cursor:
                sql_formula =  "UPDATE user_lang  SET lang = %s WHERE user_id = %s"
                cursor.execute(sql_formula, (language, user_id))
                self.connection.commit()
            
    
    def check_language(self, user_id: int) -> str:
        with self.connection.cursor() as cursor:
                sql_request = "SELECT lang FROM user_lang WHERE user_id =  %s"
                cursor.execute(sql_request, user_id)
                res = cursor.fetchone()
                print(res)
                return res.get('lang')
            
    
    def delete_user(self, user_id: int) -> None:
        with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM user_lang WHERE user_id = %s" % user_id)
                self.connection.commit()
    
    
    def save_link(self, user_id, root_link, track_link, data_time) -> None:
        # This function is not complete, will change in future commits
        with self.connection.cursor() as cursor:
                sql_formula = "INSERT INTO users (user_id, root_link, track_link, data_time ) VALUES (%s,%s,%s,%s)" 
                cursor.execute(sql_formula, (user_id, root_link, track_link, data_time))
                self.connection.commit()