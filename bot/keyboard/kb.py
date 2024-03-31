from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


is_human = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(
            text="YES",
            callback_data="positive"
        ),
        InlineKeyboardButton(
            text="NO",
            callback_data="negative"
        ),
        InlineKeyboardButton(
            text="STOP",
            callback_data="stop"
        )
    ]]
)