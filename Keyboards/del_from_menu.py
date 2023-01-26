from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  

# Buttons
button_drinks = KeyboardButton("Delete_drink")
button_main = KeyboardButton("Delete_main")
button_dessert = KeyboardButton("Delete_dessert")
button_exit = KeyboardButton("Cancel")

# Create_keyboard
kb_delete = ReplyKeyboardMarkup()
kb_delete.add(button_drinks, button_main, button_dessert, button_exit)