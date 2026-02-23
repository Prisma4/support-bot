import logging
from aiogram import types, Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from states import BotStates

router = Router()

logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def handle_start(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(BotStates.MAIN, mode=StartMode.RESET_STACK)
