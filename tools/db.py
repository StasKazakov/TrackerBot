import aiosqlite
import json
import asyncio
from datetime import datetime

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
            cur =  await db.execute("SELECT user_language FROM user_lang WHERE user_id = ?", (user_id,))
            res = await cur.fetchone()
            return ''.join(res)
    
    async def save_user_link(self, user_id: str, link: dict) -> None:
        async with aiosqlite.connect(self.db_pass) as db:
            # time =  datetime.now().strftime("%d-%m-%Y %H:%M")
            # self.save_date_time(user_id, time)
            # example =  json.dumps({'597e4b43-d995-426c-a25a-3f535624c998': 'http://link.com'})
            str = json.dumps(link)
            await db.execute("INSERT INTO Events (user_id, root_link) VALUES (?,?)", (user_id, str))
            await db.commit()
            
    async def save_date_time(self, user_id: str, date_time: str):
        async with aiosqlite.connect(self.db_pass) as db:
            await db.execute("UPDATE Events  SET date_time = ? WHERE user_id = ?", (date_time, user_id ))
            await db.commit()
    
    async def get_user_link(self, user_id: str, uuid_code: str) -> str:
        async with aiosqlite.connect(self.db_pass) as db: 
            cur =  await db.execute("SELECT root_link FROM Events WHERE user_id = ?", (user_id,))
            row = await cur.fetchone()
            res = ''.join(row)
            dict = json.loads(res)
            result = dict.get(uuid_code)
            return result
    
async def main() -> None:
    db = Database("TrackerBot.db")
    print(await db.get_user_link("660", "597e4b43-d995-426c-a25a-3f535624c998"))
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())