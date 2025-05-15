from db.db import try_register_user, SessionLocal, try_register_message
from db.models import *

from aiogram import Router, F, Bot
from aiogram.types import Message

suggestions_router = Router()

@suggestions_router.message(~F.command)
async def suggestion_handler(message: Message, bot: Bot) -> None:
    try_register_user(message.from_user.id, message.from_user.username)
    try_register_message(message.message_id, message.from_user.id, message.text if message.text else "")

    await message.answer(f"Привет, @{message.from_user.username}!\nТвое сообщение было доставлено администрации группы. Не теряй!)")
    await notify_staff(message, bot)

async def notify_staff(message: Message, bot: Bot):
    session = SessionLocal()
    try:
        for admin in session.query(User).filter_by(admin=True).all():
            await bot.send_message(admin.id,
                                   text=f"Получено предложение от @{message.from_user.username}:",
                                   parse_mode="HTML")
            await message.forward(admin.id)
    finally:
        session.close()

