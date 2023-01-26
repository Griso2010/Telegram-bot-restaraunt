from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  

# Buttons
button_upload_drink = KeyboardButton("Drink")
button_upload_dish = KeyboardButton("Main dish")
button_upload_dessert = KeyboardButton("Dessert")
button_exit = KeyboardButton("Cancel")

# Create keyboard
kb_choice_upload = ReplyKeyboardMarkup()
kb_choice_upload.add(button_upload_drink, button_upload_dish, button_upload_dessert, button_exit)