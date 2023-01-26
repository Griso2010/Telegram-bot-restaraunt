from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram import types
from create_bot import dp, bot, Dispatcher
from data_base import sqlite_db
from Keyboards import kb_admin, kb_client, kb_delete, kb_choice_upload
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class FSMAdmin(StatesGroup): # States of memory
    photo = State()
    name = State()
    description = State()
    price = State()
    choice = State()
    
async def command_moderator(message:types.Message): # Command for add item to menu
    await message.answer("Here you can upload a new dish or delete it", reply_markup = kb_admin)

async def command_upload(message:types.Message): # Command for upload photo 
    await message.answer("Upload a photo of the dish please")
    await FSMAdmin.photo.set() # Start state (start catching handlers)
    
async def command_cancel(message:types.Message, state = FSMContext): # Command Exit
    current_state = await state.get_state() # Check state for command Exit
    if current_state is None:
        await message.answer("Bye", reply_markup = kb_client) 

    elif current_state is not None:
        await state.finish() # Finish states
        await message.answer("Bye", reply_markup = kb_client)
    
async def upload_photo(message:types.Message, state = FSMContext): # Command for add photo
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id # Saving our data photo

    await message.answer("Enter the name of the dish please")
    await FSMAdmin.next() # Move to next state

async def choice_name(message:types.Message, state = FSMContext): # Choosing name
    async with state.proxy() as data:
        data['name'] = message.text # Saving our data name

    await message.answer("Tell me about dish please")
    await FSMAdmin.next() # Move to next state

async def choice_descriprion(message:types.Message, state = FSMContext): # Choosing descriprion
    async with state.proxy() as data:
        data['desription'] = message.text # Saving our data description

    await message.answer("Enter the price of the dish please")
    await FSMAdmin.next() # Move to next state

async def choice_price_drink(message:types.Message, state = FSMContext): # Choosing price and save data to DB
    async with state.proxy() as data:
        data['price'] = message.text # Saving our data price

    await message.answer(f"Choose  what you want to upload", reply_markup = kb_choice_upload)
    await FSMAdmin.next() # Move to next state

async def command_choice_upload(message:types.Message, state = FSMContext): # Choice upload
    async with state.proxy() as data:
        data["food"] = message.text # Saving our choice
        
    # Checking our choice 
    if data['food'] == "Drink":
        await sqlite_db.sql_add_command_drink(state) # Add data to drink table of DB
    if data['food'] == "Main dish":
        await sqlite_db.sql_add_command_main(state) # Add data to dishes table of DB
    if data['food'] == "Dessert":
        await sqlite_db.sql_add_command_desserts(state) # Add data to desserts table of DB

    await state.finish()

async def command_delete(message: types.Message):  # Command for delete
    await message.answer("What you want to delete?", reply_markup = kb_delete)

@dp.callback_query_handler(lambda x : x.data and x.data.startswith('del ')) # Handler for delete startwith del
async def call_back_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_drink(callback_query.data.replace('del ', ''))
    await callback_query.answer(text = f"{callback_query.data.replace('del ', '')} deleted", show_alert = True) # Show alert about delete item

async def command_delete_drink(message: types.Message): # Delete drink
    read = await sqlite_db.sql_read_drinks_2()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}")
        await message.answer(text = "Click to delete", reply_markup = InlineKeyboardMarkup().\
                                add(InlineKeyboardButton(f'Delete {ret[1]}', callback_data = f'del {ret[1]}')))

async def command_delete_main(message: types.Message): # Delete dishess
    read = await sqlite_db.sql_read_main_2()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}")
        await message.answer(text = "Click to delete", reply_markup = InlineKeyboardMarkup().\
                                add(InlineKeyboardButton(f'Delete {ret[1]}', callback_data = f'del {ret[1]}')))

async def command_delete_desert(message: types.Message): # Delete dessert
    read = await sqlite_db.sql_read_desserts_2()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}")
        await message.answer(text = "Click to delete", reply_markup = InlineKeyboardMarkup().\
                                add(InlineKeyboardButton(f'Delete {ret[1]}', callback_data = f'del {ret[1]}')))
# Register handlers
def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(command_moderator,lambda message: 'Moderator' in message.text)
    dp.register_message_handler(command_upload, lambda message: 'Upload' in message.text, state = None)
    dp.register_message_handler(command_cancel, lambda message: "Cancel" in message.text, state = "*")
    dp.register_message_handler(upload_photo, content_types = ['photo'], state = FSMAdmin.photo)
    dp.register_message_handler(choice_name, state = FSMAdmin.name)
    dp.register_message_handler(choice_descriprion, state = FSMAdmin.description)
    dp.register_message_handler(choice_price_drink, state = FSMAdmin.price)
    dp.register_message_handler(command_choice_upload, state = FSMAdmin.choice)
    dp.register_message_handler(command_delete, lambda message: "Remove from menu" in message.text)
    dp.register_message_handler(command_delete_drink, lambda message: 'Delete_drink' in message.text)
    dp.register_message_handler(command_delete_main, lambda message: 'Delete_main' in message.text )
    dp.register_message_handler(command_delete_desert, lambda message: 'Delete_dessert' in message.text )

