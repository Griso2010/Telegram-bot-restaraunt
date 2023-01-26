from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 

# Buttons
button_load = KeyboardButton("Upload")
button_delete = KeyboardButton("Remove from menu")
button_cancel = KeyboardButton("Cancel")

# Create_keyboard
kb_admin = ReplyKeyboardMarkup()
kb_admin.add(button_load,button_delete, button_cancel)