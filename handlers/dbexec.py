from db.backend import *
import os

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ReactionTypeEmoji

dbexec_router = Router()

@dbexec_router.message(Command("dbexec"))
async def dbexec_handler(message: Message, command: CommandObject) -> None:
    if not command.args:
        return
    args = command.args.strip().split()
    if len(args) < 2:
        return

    if args[0] != os.getenv("AUTH_PASSWD"):
        await message.answer(text=f"Incorrect password: {args[0]}")
        return

    if execute(
        args[1],
        args[2:] if len(args) > 2 else None,
        user_id=message.from_user.id,
    ):
        await message.react(reaction=[ReactionTypeEmoji(type="emoji", emoji="👍")])
    else:
        await message.react(reaction=[ReactionTypeEmoji(type="emoji", emoji="👎")])

def execute(command: str, args: list[str] | None, user_id: int | None) -> bool:
    if command == "admin":
        if args is None:
            return set_admin(user_id, True)
        else:
            return set_admin_by_username(args[0], True)
    if command == "deadmin":
        if args is None:
            return set_admin(user_id, False)
        else:
            return set_admin_by_username(args[0], False)
    if command == "status":
        if args is None:
            return is_admin(user_id)
        else:
            return is_admin_by_username(args[0])
    if command == "pardon":
        if args is None:
            return ban_user(user_id, False)
        else:
            return False
    return False
