import os

from aiogram.filters import Filter
from aiogram.types import Message

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# List of admins
ADMINS = [int(os.getenv('ADMIN_ID'))]


# Admin filter
class AdminFilter(Filter):
    def __init__(self):
        self.admins = ADMINS
    
    async def __call__(self, message: Message):
        return message.from_user.id in self.admins
