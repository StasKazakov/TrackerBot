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
            cur = await db.execute("SELECT user_language FROM user_lang WHERE user_id = ?", (user_id,))
            res = await cur.fetchone()
            return ''.join(res)

    async def save_user_link(self, user_id: str, orig_link: str, link_id: str, link_name: str) -> None: # Save user_link to db
        async with aiosqlite.connect(self.db_pass) as db:
            await db.execute("INSERT INTO links (link_id, user_id, orig_link, link_name) VALUES (?,?,?,?)", (link_id, user_id, orig_link, link_name))
            await db.commit()
    
    async def get_user_link(self, link_id: str) -> str: # Get user link
        async with aiosqlite.connect(self.db_pass) as db: 
            cur =  await db.execute("SELECT orig_link FROM links WHERE link_id = ?", (link_id,))
            row = await cur.fetchone()
            if row is None:
                return "No link for this link_id"
            else:
                return ''.join(row)
            
    async def get_names_link(self, user_id: str) -> list: 
        async with aiosqlite.connect(self.db_pass) as db: 
            cur =  await db.execute("SELECT link_name FROM links WHERE user_id = ?", (user_id,))
            row = await cur.fetchall() 
            list = []
            for names in row:
                    list.append(''.join(names))
            return list
       
    async def check_name_link(self, user_id: str, link_name: str) -> bool:
         async with aiosqlite.connect(self.db_pass) as db:
            cur =  await db.execute("SELECT link_name FROM links WHERE user_id = ?", (user_id,))
            res = await cur.fetchall() 
            list = []
            for names in res:
                    list.append(''.join(names))
            if link_name in list:
                return True
            elif link_name not in list:
                return False
         
    async def save_date_time(self, link_id: str, date_time: str) -> None: # Save date_time to db
        async with aiosqlite.connect(self.db_pass) as db:
            await db.execute("INSERT INTO links (link_id, counter) VALUES (?,?)", (link_id, date_time))
            await db.commit()
            
    async def get_counter(self, link_id):
        async with aiosqlite.connect(self.db_pass) as db:
            cur = await db.execute("SELECT counter FROM Events WHERE link_id = ? ", (link_id,))
            res = await cur.fetchall()
            # will be changed in future commits
