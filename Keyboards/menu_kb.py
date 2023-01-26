from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  

# Buttons
button_drinks = KeyboardButton("Drinks")
button_main_dishes = KeyboardButton("Main_dishes")
button_desserts = KeyboardButton("Desserts")
button_exit = KeyboardButton("Exit")

# Create_keyboard
kb_menu = ReplyKeyboardMarkup()
kb_menu.add(button_drinks,button_main_dishes,button_desserts,button_exit)