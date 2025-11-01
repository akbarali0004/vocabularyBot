from aiogram import types, F, Router, Bot
from aiogram.filters import Command

from filters import IsAdminFilter


router = Router()
router.message.filter(IsAdminFilter())
router.callback_query.filter(IsAdminFilter())


@router.message(Command("admin"))
async def admin_panel(message: types.Message, bot:Bot):
    await message.answer("Welcome to the admin panel!")