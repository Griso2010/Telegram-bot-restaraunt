from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN

# Create storage
storage = MemoryStorage()

# Token of bot
bot = Bot(token = TOKEN)

dp = Dispatcher(bot, storage = storage) 
