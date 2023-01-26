import sqlite3 as sq
from create_bot import bot
import os

READ_DRINKS = "SELECT * FROM drinks"
READ_DISHES = "SELECT * FROM main"
READ_DESSERT = "SELECT * FROM desserts"


def sql_start(): # Connection and cheking DB
    global base, cur 
    base = sq.connect(os.path.realpath('./data_base/menu.db')) # PATH to DB
    

    cur = base.cursor()
    if base:
        print("Data base of menu connected OK")

    # Create tables 
    CREATE_DRINKS = "CREATE TABLE IF NOT EXISTS drinks(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)"
    CREATE_DISHES = "CREATE TABLE IF NOT EXISTS main(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)"
    CREATE_DESSERTS = "CREATE TABLE IF NOT EXISTS desserts(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)"

    base.execute(CREATE_DRINKS) 
    base.commit()
    base.execute(CREATE_DISHES)
    base.commit()
    base.execute(CREATE_DESSERTS)
   
async def sql_add_command_drink(state): # Add drink to DB
    async with state.proxy() as data:
        del data['food'] # Delete our choice
        cur.execute("INSERT INTO drinks VALUES(?, ?, ?, ?)",tuple(data.values()))
        base.commit()
    
async def sql_add_command_main(state): # Add dish to DB
    async with state.proxy() as data:
        del data['food'] # Delete our choice
        cur.execute("INSERT INTO main VALUES(?, ?, ?, ?)",tuple(data.values()))
        base.commit()

async def sql_add_command_desserts(state): # Add desert to DB
    async with state.proxy() as data:
        del data['food'] # Delete our choice
        cur.execute("INSERT INTO desserts VALUES(?, ?, ?, ?)",tuple(data.values()))
        base.commit()

async def sql_read_drinks(message): # Sending drinks from DB
    for ret in cur.execute(READ_DRINKS).fetchall():
        await bot.send_photo(chat_id = message.from_user.id, photo = ret[0])
        await message.answer(f"Name: {ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}")
        
async def sql_read_main_dishes(message): # Sending dishes from DB
    for ret in cur.execute(READ_DISHES).fetchall():
        await bot.send_photo(chat_id = message.from_user.id, photo = ret[0])
        await message.answer(f"Name: {ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}")

async def sql_read_desserts(message): # Sending desserts from DB
    for ret in cur.execute(READ_DESSERT).fetchall():
        await bot.send_photo(chat_id = message.from_user.id, photo = ret[0])
        await message.answer(f"Name: {ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}")

async def sql_delete_drink(data): # Delete drink from DB
    cur.execute("DELETE FROM drinks WHERE name = ?", (data,))
    base.commit()

async def sql_delete_dish(data): # Delete dish from DB
    cur.execute("DELETE FROM main WHERE name = ?", (data,))
    base.commit()

async def sql_delete_dessert(data): # Delete dessert from DB
    cur.execute("DELETE FROM desserts WHERE name = ?", (data,))
    base.commit()

async def sql_read_drinks_2(): # Only reading drinks from DB
    return  cur.execute(READ_DRINKS)

async def sql_read_main_2(): # Only reading dishes from DB
    return  cur.execute(READ_DISHES)

async def sql_read_desserts_2(): # Only reading desserts from DB
    return  cur.execute(READ_DESSERT)

