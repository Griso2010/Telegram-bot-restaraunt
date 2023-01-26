from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from Keyboards import kb_client, kb_review, kb_menu
import datetime
from data_base import sqlite_db_reviews, sqlite_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

PLACE = "26-34 Emerald St, London WC1N 3QA, UK"
help_commands = """
/Help 
/Place 
/Working_hours
/Menu 
/Reviews 
/Moderator (Add or delete menu item)
"""

class FSMclient(StatesGroup): #States of memory
    write = State()

async def command_start(message:types.Message): # Command welcome
    await message.answer(text = "Welcome to the Cheff Bot ❤️ ", reply_markup = kb_client) 

async def command_help(message:types.Message): #Command help
    await message.answer(text = help_commands)

async def command_place(message:types.Message): # Command send place and geo
    await message.answer(text = PLACE)
    await bot.send_location(chat_id = message.from_user.id, latitude = 51.521727, longitude = -0.117255) 

async def command_work(message:types.Message): # Command hours of work
    now = datetime.datetime.now() # Time now
    day = now.strftime("%A") # Which day today
    # Cheking which day now and answer about hours of working
    if day == "Thursday" or day == "Friday":
        await message.answer(text = f"Today is {day}, we are openfrom 10:00 to 22:30")
    if day == "Monday" or day == "Tuesday" or day == "Wensday":
        await message.answer(text = f"Today is {day}, we are open from 8:00 до 22:00")
    if day == "Sunday" or day == "Saturday":
        await message.answer(text = f"Today is {day}, we are open from 17:00 to 02:00")

async def command_reviews(message:types.Message): # Command to choose to see or write review
    await message.answer("Please choose one option", reply_markup = kb_review)
    
@dp.callback_query_handler(lambda x : x.data and x.data.startswith('del ')) # Handler for delete startwith del
async def call_back_run(callback_query: types.CallbackQuery):
    await sqlite_db_reviews.sql_delete_review(callback_query.data.replace('del ', ''))
    await callback_query.answer(text = f"{callback_query.data.replace('del ', '')} deleted", show_alert = True) # Show alert about delete review

async def command_delete_review(message: types.Message): # Delete review
    read = await sqlite_db_reviews.sql_read_reviews() # Reading all reviews
    for ret in read:
        await message.answer(*ret)
        await message.answer(text = "Click to delete", reply_markup = InlineKeyboardMarkup().\
                                add(InlineKeyboardButton(f'Delete {ret[0]}', callback_data = f'del {ret[0]}')))

async def command_to_write(message:types.Message): # Start state write review
    await message.answer("Please write your impression about us")
    await FSMclient.write.set() # Start state (start catching handlers)

async def command_exit(message:types.Message, state = FSMContext):# Command Exit
    current_state = await state.get_state() # Check state for command Exit
    if current_state is None:
        await message.answer("Bye", reply_markup = kb_client)

    elif current_state is not None:
        await state.finish()
        await message.answer("OK", reply_markup = kb_client)

async def command_write(message:types.Message, state = FSMContext): # Write review
    async with state.proxy() as data_reviews:
        data_reviews['review'] = message.text # Saving our data review

    await sqlite_db_reviews.sql_add_command(state) # Add review to DB
    await state.finish() # FInish state

async def command_read(message:types.Message): # Read review
    await sqlite_db_reviews.sql_read(message) # Reading reviews from DB

async def command_menu(message:types.Message): #Menu
    await message.answer("Please choose what you want", reply_markup = kb_menu)

async def command_drinks(message:types.Message): # Drinks from menu
    await sqlite_db.sql_read_drinks(message) # Reading drinks from DB

async def command_main_dishes(message:types.Message): # Dishes from menu
    await sqlite_db.sql_read_main_dishes(message) # Reading dishes from DB

async def command_desserts(message:types.Message): # Desserts from menu
    await sqlite_db.sql_read_desserts(message) # Reading desserts from DB
# Register all handlers
def register_handlers_client(dp:Dispatcher):
    dp.register_message_handler(command_start, commands = ["Start"])
    dp.register_message_handler(command_help, lambda message: 'Help' in message.text)
    dp.register_message_handler(command_place, lambda message: 'Place' in message.text)
    dp.register_message_handler(command_work, lambda message: 'Working hours' in message.text)
    dp.register_message_handler(command_reviews, lambda message: "Reviews" in message.text)
    dp.register_message_handler(command_delete_review, lambda message: "Delete_review" in message.text)
    dp.register_message_handler(command_to_write,lambda message: "Write review" in message.text, state = None )
    dp.register_message_handler(command_exit, lambda message: "Exit" in message.text)
    dp.register_message_handler(command_write, state = FSMclient.write)
    dp.register_message_handler(command_read, lambda message: "See reviews" in message.text)
    dp.register_message_handler(command_menu, lambda message: 'Menu' in message.text)
    dp.register_message_handler(command_drinks, lambda message: "Drinks" in message.text)
    dp.register_message_handler(command_main_dishes, lambda message: "Main_dishes" in message.text)
    dp.register_message_handler(command_desserts, lambda message: "Desserts" in message.text)
