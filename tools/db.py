import aiosqlite


class Database:

    def __init__(self, db_pass: str):
        self.db_pass = db_pass
        
    async def add_user(self, user_id: str, name_tg: str) -> None:
        async with aiosqlite.connect(self.db_pass) as db:
            cursor = await db.execute("SELECT user_id FROM user_lang WHERE user_id = ?", (user_id,))
            res = await cursor.fetchall()
            if bool(len(res)) == False:
                await db.execute("INSERT INTO user_lang (user_id, name_tg) VALUES (?,?)", (user_id, name_tg ))
                await db.commit()
            else:
                pass
    
    async def save_language(self, user_id: str, language: str) -> None: # Saving chose language to database  
        async with aiosqlite.connect(self.db_pass) as db:
            await db.execute("UPDATE user_lang  SET user_language = ? WHERE user_id = ?", (language, user_id ))
            await db.commit()
            
    async def check_language(self, user_id: str) -> str:  # Function will check ordered language
        async with aiosqlite.connect(self.db_pass) as db:
            cur = await db.execute("SELECT user_language FROM user_lang WHERE user_id = ?", (user_id,))
            res = await cur.fetchone()
            return ''.join(res)
    
    async def save_user_link(self, user_id: str, user_link: str, uuid_code: str) -> None:

        async with aiosqlite.connect(self.db_pass) as db:
            pass
        
    async def save_date_time(self, user_id: str, data_time: str):
        async with aiosqlite.connect(self.db_pass) as db:
            pass
        

    