from create_bot import bot
import sqlite3 as sq
import os

READ_TABLE = "SELECT * FROM reviews"

def sql_start(): # Connection and cheking DB
    global base,cur
    base = sq.connect(os.path.realpath('./data_base/reviews.db'))
    cur = base.cursor()

    if base:
        print("Data base of reviews connected OK")
    CREATE_TABLE = "CREATE TABLE IF NOT EXISTS reviews(description TEXT PRIMARY KEY)"
    base.execute(CREATE_TABLE)
    base.commit()

async def sql_add_command(state): # Insert values into DB
    async with state.proxy() as data_reviews:
        cur.execute("INSERT INTO reviews VALUES(?)", tuple(data_reviews.values()))
        base.commit()

async def sql_read(message): # Read DB and send all
   for i in cur.execute(READ_TABLE).fetchall():
    await message.answer(*i)

async def sql_read_reviews(): # Only reading DB
    return cur.execute(READ_TABLE)

async def sql_delete_review(data): # Delete item from DB
    cur.execute("DELETE FROM reviews WHERE description = ?", (data, ))
    base.commit()