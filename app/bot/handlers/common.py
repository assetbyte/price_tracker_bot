from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "<b> Available commands:</b>\n\n"
        "<b>Tracking management:</b>\n"
        "/new_tracking — Create new tracking\n"
        "/my_trackings — View my active trackings\n"
        "/edit_tracking — Edit tracking parameters\n"
        "/delete_specific_tracking — Delete tracking by ID\n"
        "/delete_all_trackings — Delete all trackings\n\n"
        "<b>General commands:</b>\n"
        "/cancel — Cancel current action\n"
        "/help — Show this message"
    )
    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("You have no active actions to cancel")
        return

    await state.clear()
    await message.answer("Action cancelled. You can start a new action now.")
