import os

import aiosqlite as sq


# app.py joylashgan papkani aniqlaymiz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Shu papkaga nisbatan data/base.db faylini ko‘rsatamiz
DATABASE = os.path.join(BASE_DIR, "data", "base.db")

# DATABASE = "data/base.db"
async def db_start():
    async with sq.connect(DATABASE) as db:
        await db.execute("PRAGMA foreign_keys = ON;")  # foreign key larni yoqish

        await db.execute("""CREATE TABLE IF NOT EXISTS users(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         nik_name TEXT NOT NULL,
                         username TEXT,
                         tg_id INTEGER NOT NULL UNIQUE,
                         created_at TEXT DEFAULT (datetime('now', '+5 hours')),
                         is_active INTEGER DEFAULT 1);""")
        
        await db.execute("""CREATE INDEX IF NOT EXISTS idx_users_tg_id 
                         ON users(tg_id);""")
        

        await db.execute("""CREATE TABLE IF NOT EXISTS category(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         title TEXT NOT NULL,
                         author_id INTEGER NOT NULL,
                         FOREIGN KEY (author_id) REFERENCES users(tg_id))""")


        await db.execute("""CREATE TABLE IF NOT EXISTS words(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         en_word TEXT NOT NULL,
                         uz_word TEXT NOT NULL,
                         author_id INTEGER NOT NULL,
                         category INTEGER NOT NULL,
                         FOREIGN KEY (author_id) REFERENCES users(tg_id),
                         FOREIGN KEY (category) REFERENCES category(id) ON DELETE CASCADE);""")
        
        
        # await db.execute("""CREATE TABLE IF NOT EXISTS quiz_results(
        #                  id INTEGER RIMARY KEY AUTOINCREMENT,
        #                  user_id INTEGER NOT NULL,
        #                  category INTEGER NOT NULL)""")
        
        await db.commit()


#add user
async def save_user(nik_name, username, tg_id):
    async with sq.connect(DATABASE) as db:
        cursor = await db.execute("SELECT tg_id FROM users WHERE tg_id=?", (tg_id,))
        user = await cursor.fetchone()

        if not user:
            await db.execute("INSERT INTO users (nik_name, username, tg_id) VALUES(?, ?, ?);", (nik_name, username, tg_id))
            await db.commit()


#create catagory
async def add_category(title, author_id):
    async with sq.connect(DATABASE) as db:
        await db.execute("INSERT INTO category (title, author_id) VALUES(?, ?);", (title, author_id))
        await db.commit()
    async with sq.connect(DATABASE) as db:
        cat_id = await db.execute("SELECT id FROM category WHERE title = ? AND author_id = ? ORDER BY id DESC LIMIT 1;", (title, author_id))
        return await cat_id.fetchone()

#get category
async def get_category(author_id):
    async with sq.connect(DATABASE) as db:
        categories = await db.execute("SELECT id, title FROM category WHERE author_id=?", (author_id,))
        return await categories.fetchall()


#so'zlarni saqlash
async def add_words(en_word, uz_word, author_id, category):
    async with sq.connect(DATABASE) as db:
        await db.execute("INSERT INTO words (en_word, uz_word, author_id, category) VALUES(?, ?, ?, ?);", (en_word, uz_word, author_id, category))
        await db.commit()

#sozlarni olish
async def get_words(category, author_id):
    async with sq.connect(DATABASE) as db:
        cur = await db.execute("""SELECT en_word, uz_word
                               FROM words WHERE category = ? AND author_id = ?;""", (category, author_id))
        words = await cur.fetchall()
        return words
    