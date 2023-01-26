from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  

# Buttons
button_write = KeyboardButton("Write review")
button_read = KeyboardButton("See reviews")
button_exit = KeyboardButton("Exit")
button_delete = KeyboardButton("Delete_reviews")

# Create_keyboard
kb_review = ReplyKeyboardMarkup()
kb_review.add(button_write,button_read, button_exit, button_delete)