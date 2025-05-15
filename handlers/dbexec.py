from db.models import *
from db.db import SessionLocal
import os

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

class DbexecCommandExecutionException(Exception):
    ...

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

    try:
        if execute(
            args[1],
            args[2:] if len(args) > 2 else None,
            username=message.from_user.username,
        ):
            await message.answer(text="Command executed successfully")
        else:
            await message.answer(text="Command failed to execute")
    except DbexecCommandExecutionException as exception:
        await message.answer(text=f"Exception while executing command: {exception}")

def execute(command: str, args: list[str] | None, username: str | None) -> bool:
    session = SessionLocal()
    try:
        if command == "admin":
            if args is None:
                # admin the one who wrote it
                user = session.query(User).filter_by(username=username).first()
                if user is None:
                    raise DbexecCommandExecutionException("User not found")
                user.admin = True
                session.commit()
            else:
                # admin args[0]
                user = session.query(User).filter_by(username=args[0]).first()
                if user is None:
                    raise DbexecCommandExecutionException("User not found")
                user.admin = True
                session.commit()
        if command == "deadmin":
            if args is None:
                user = session.query(User).filter_by(username=username).first()
                if user is None:
                    raise DbexecCommandExecutionException("User not found")
                user.admin = False
                session.commit()
            else:
                user = session.query(User).filter_by(username=username).first()
                if user is None:
                    raise DbexecCommandExecutionException("User not found")
                user.admin = False
                session.commit()
        if command == "getinfo":
            if args is None:
                # Return info about the one who's asking
                raise DbexecCommandExecutionException("Not yet implemented")
            else:
                # Return info about args[0]
                raise DbexecCommandExecutionException("Not yet implemented")
        return True
    except DbexecCommandExecutionException as e:
        raise e
    finally:
        session.close()
