from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin
from data_base import sqlite_db,  sqlite_db_reviews


async def on_startup(_): # Start data base and run bot
    print("Bot is online")
    sqlite_db.sql_start()
    sqlite_db_reviews.sql_start()

# Register handlers from handlers
client.register_handlers_client(dp) 
admin.register_handlers_admin(dp)

# Start polling
executor.start_polling(dp, skip_updates = True, on_startup = on_startup)
	



