from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from db.backend import *

import re

ban_router = Router()
mention_pattern = re.compile(r"@\w+")

@ban_router.message(Command("ban"))
async def ban_command_handler(message: Message, command: CommandObject):
    await process_operation(message, command, True)

@ban_router.message(Command("unban"))
async def unban_command_handler(message: Message, command: CommandObject):
    await process_operation(message, command, False)

async def process_operation(message: Message, command: CommandObject, status: bool):
    """
    Универсальная функция, в которой обрабатывается логика бана и разбана
    :param message:
    :param command:
    :param status:
    :return:
    """
    global mention_pattern
    if not is_admin(message.from_user.id):
        return
    args = command.args
    if args is None:
        await message.reply("You didn't specify who the fuck I should ban")
    else:
        args = args.strip()
        for mention in re.findall(mention_pattern, args):
            if ban_user_by_username(mention.replace("@", ""), status):
                await message.reply(f"successfully banned {mention}")
            else:
                await message.reply(f"failed to ban {mention}")
