from db.backend import *
from db.models import *

from aiogram import Router, F, Bot
from aiogram.types import Message, ReactionTypeEmoji

suggestions_router = Router()

@suggestions_router.message(~F.command)
async def suggestion_handler(message: Message, bot: Bot) -> None:
    if not is_admin(message.from_user.id):
        try_register_user(message.from_user.id, message.from_user.username)
        original_message_id = register_original_message(message.message_id, message.from_user.id, message.text if message.text else "")
        if not original_message_id:
            await message.react(reaction=[ReactionTypeEmoji(type="emoji", emoji="👎")])
            return

        await notify_staff(message, bot, original_message_id)
    else:
        print(message.message_thread_id)
    await message.react(reaction=[ReactionTypeEmoji(type="emoji", emoji="👍")])

async def notify_staff(message: Message, bot: Bot, original_message_id: int):
    session = SessionLocal()
    try:
        for admin in session.query(User).filter_by(admin=True).all():
            await bot.send_message(admin.id,
                                   text=f"Получено предложение от @{message.from_user.username}:",
                                   parse_mode="HTML")
            fwd_message = await message.forward(admin.id)
            register_forwarded_message(fwd_message.message_id, fwd_message.chat.id, original_message_id)
    finally:
        session.close()
