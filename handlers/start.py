from db.db import try_register_user

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    try_register_user(message.chat.id, message.from_user.username)
    await message.answer("Ну, привет, это бот-предложка для канала https://t.me/sharedpcb")
