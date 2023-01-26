from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  

# Buttons
button_help = KeyboardButton("Help")
button_place = KeyboardButton("Place")
button_hours = KeyboardButton("Working hours")
button_menu = KeyboardButton("Menu")
button_reviews = KeyboardButton("Reviews")
button_admin = KeyboardButton("Moderator")

# Create_keyboard
kb_client = ReplyKeyboardMarkup()
kb_client.add(button_help, button_place, button_hours, button_menu, button_reviews, button_admin)
