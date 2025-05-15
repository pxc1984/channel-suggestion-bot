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
        if message.reply_to_message is None:
            return
        original_message_id = get_original_message_from_forwarded(
            message.reply_to_message.chat.id,
            message.reply_to_message.message_id
        )
        if original_message_id is False:
            return
        await message.copy_to(original_message_id['from_user'])
    await message.react(reaction=[ReactionTypeEmoji(type="emoji", emoji="✍")])

async def notify_staff(message: Message, bot: Bot, original_message_id: int):
    session = SessionLocal()
    try:
        for admin in session.query(User).filter_by(admin=True).all():
            await bot.send_message(admin.id,
                                   text=f"Получено предложение от @{message.from_user.username}:",
                                   parse_mode="HTML")
            fwd_message = await message.copy_to(admin.id)
            register_forwarded_message(fwd_message.message_id, admin.id, original_message_id)
    finally:
        session.close()
