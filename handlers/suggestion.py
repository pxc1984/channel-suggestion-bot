from aiogram.utils.text_decorations import MarkdownDecoration

from db.db import try_register_user, SessionLocal
from db.models import *

from aiogram import Router, F, Bot
from aiogram.types import Message

suggestions_router = Router()

@suggestions_router.message(~F.command)
async def suggestion_handler(message: Message, bot: Bot) -> None:
    try_register_user(message.chat.id, message.from_user.username)
    await message.answer(f"Привет, @{message.from_user.username}!\nТвое сообщение было доставлено администрации группы. Не теряй!)")
    await notify_staff(message, bot)

async def notify_staff(message: Message, bot: Bot):
    session = SessionLocal()
    try:
        for admin in session.query(User).filter_by(admin=True).all():
            await bot.send_message(admin.chat_id,
                                   text=f"Получено предложение от @{message.from_user.username}:",
                                   parse_mode="HTML")
            await message.forward(admin.chat_id)
    finally:
        session.close()

