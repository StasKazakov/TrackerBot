import aiosqlite
from datetime import datetime

class Database:

    def __init__(self):
        self.db_pass: str = "TrackerBot.db"
        
    async def add_user(self, user_id: str, name_tg: str) -> bool:
        async with aiosqlite.connect(self.db_pass) as db:
            res = await db.execute_fetchall("SELECT user_id FROM user_lang WHERE user_id = ?", (user_id,))
            if bool(len(res)) == False:
                await db.execute("INSERT INTO user_lang (user_id, name_tg) VALUES (?,?)", (user_id, name_tg ))
                await db.commit()
                return False
            else:
                return True
    
    async def save_language(self, user_id: str, language: str) -> None: # Saving chose language to database
        async with aiosqlite.connect(self.db_pass) as db:               # accepts such parameters: user_id, lang
            await db.execute("UPDATE user_lang  SET user_language = ? WHERE user_id = ?", (language, user_id ))
            await db.commit()
            
    async def check_language(self, user_id: str) -> str:  # Function will check ordered language, accepts such parameters: user_id
        async with aiosqlite.connect(self.db_pass) as db:
            cur = await db.execute("SELECT user_language FROM user_lang WHERE user_id = ?", (user_id,))
            res = await cur.fetchone()
            return ''.join(res)

    async def save_user_link(self, user_id: str, orig_link: str, link_id: str, link_name: str) -> None: # Save user_link to db
        async with aiosqlite.connect(self.db_pass) as db:                        # accepts such parameters: user_id, orig_link, link_id, link_name
            await db.execute("INSERT INTO links (link_id, user_id, orig_link, link_name) VALUES (?,?,?,?)", (link_id, user_id, orig_link, link_name))
            await db.commit()
    
    async def get_user_link(self, link_id: str) -> str: # Get user link, accepts such parameters: link_id
        async with aiosqlite.connect(self.db_pass) as db: 
            cur =  await db.execute("SELECT orig_link FROM links WHERE link_id = ?", (link_id,))
            row = await cur.fetchone()
            if row is None:
                return "No link for this link_id"
            else:
                return ''.join(row)
            
    async def get_names_link(self, user_id: str) -> list: # Get all user links names, accepts such parameters: user_id
        async with aiosqlite.connect(self.db_pass) as db: 
            row =  await db.execute_fetchall("SELECT link_name FROM links WHERE user_id = ?", (user_id,)) 
            list = []
            for names in row:
                    list.append(''.join(names))
            return list
       
    async def check_name_link(self, user_id: str, link_name: str) -> bool: # Checked link name from user in db
         async with aiosqlite.connect(self.db_pass) as db:       # accepts such parameters: user_id, link_name
            res =  await db.execute_fetchall("SELECT link_name FROM links WHERE user_id = ?", (user_id,))
            list = []
            for names in res:
                    list.append(''.join(names))
            if link_name in list:
                return True
            elif link_name not in list:
                return False
         
    async def save_date_time(self, link_id: str, date_time: str) -> None: # Save date_time to db
        async with aiosqlite.connect(self.db_pass) as db:        # accepts such parameters: link_id, date_time
            await db.execute("INSERT INTO links (link_id, counter) VALUES (?,?)", (link_id, date_time))
            await db.commit()
    
    async def save_request(self, user_id: str, request_text: str, request_name: str)-> None: # Save user request to db
        async with aiosqlite.connect(self.db_pass) as db:    # accepts such parameters: user_id, request_text, request_name
            await db.execute("INSERT INTO requests (user_id, request_text, request_name) VALUES (?,?,?)", (user_id, request_text, request_name))
            await db.commit()
      
    async def get_all_counters(self, link_id): # Get all counters from db, accepts such parameters: link_id
        async with aiosqlite.connect(self.db_pass) as db:
            res = await db.execute_fetchall("SELECT counter FROM Events WHERE link_id = ? ", (link_id,))
            return len(res)
        
    async def get_link_id(self, link_name): # Get link_id from db by link_name, accepts such parameters: link_name
        async with aiosqlite.connect(self.db_pass) as db:
            cur = await db.execute("SELECT link_id FROM links WHERE link_name = ?", (link_name,))
            row = await cur.fetchone()
            return  ''.join(row)
        
    async def get_counters_by_data(self, link_id, data_from, data_to): # Get user counters by data_time
        async with aiosqlite.connect(self.db_pass) as db: # accepts such parameters: link_id, data_from, data_to
            res = await db.execute_fetchall("SELECT counter FROM Events WHERE link_id = ? AND counter BETWEEN ? AND ?", (link_id, data_from, data_to))
            return len(res)
            