from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from db.backend import *

import re
import enum

class BanOperationResult(enum.Enum):
    Success = 0
    Failure = 1
    WrongSyntax = 2
    WrongPrivilege = 3
    Unknown = 4

ban_router = Router()
mention_pattern = re.compile(r"@\w+")

@ban_router.message(Command("ban"))
async def ban_command_handler(message: Message, command: CommandObject):
    _result = process_operation(message, command, True)
    await message.answer(f"{_result.name}")

@ban_router.message(Command("unban"))
async def unban_command_handler(message: Message, command: CommandObject):
    _result = process_operation(message, command, False)
    await message.answer(f"{_result.name}")

def process_operation(message: Message, command: CommandObject, status: bool) -> BanOperationResult:
    """
    Универсальная функция, в которой обрабатывается логика бана и разбана
    :param message:
    :param command:
    :param status:
    :return:
    """
    global mention_pattern
    if not is_admin(message.from_user.id):
        return BanOperationResult.WrongPrivilege
    args = command.args
    if args is None:
        return BanOperationResult.WrongSyntax
    else:
        args = args.strip()
        for mention in re.findall(mention_pattern, args):
            if ban_user_by_username(mention.replace("@", ""), status):
                return BanOperationResult.Success
            else:
                return BanOperationResult.Failure
        return BanOperationResult.Unknown
