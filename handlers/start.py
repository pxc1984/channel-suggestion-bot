import os

from db.backend import try_register_user

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()
CHANNEL_NAME = os.getenv("CHANNEL_NAME")
if CHANNEL_NAME is None:
    CHANNEL_NAME = "https://t.me/sharedpcb"


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    try_register_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Ну, привет, это бот-предложка для канала {CHANNEL_NAME}")
