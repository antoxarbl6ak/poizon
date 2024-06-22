from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="catalog", callback_data="catalog"),
     InlineKeyboardButton(text="shipment", callback_data="shipment")],
    [InlineKeyboardButton(text="rates", url="https://kompege.ru"),
     InlineKeyboardButton(text="help", url="https://jut.su/samurai-champlo")],
    [InlineKeyboardButton(text="info", callback_data="info")]
])

back_to_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="back", callback_data="back_to_start")]
])

admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="add pair", callback_data="add_pair"),
     InlineKeyboardButton(text="remove pair", callback_data="remove_pair")]
])

back_to_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="back", callback_data="back_to_admin")]
])

add_pair_ensure = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="correct", callback_data="add_pair_correct"),
     InlineKeyboardButton(text="wrong", callback_data="add_pair_wrong")]
])


async def catalog_brands(brands):
    kb = InlineKeyboardBuilder()
    for brand in brands:
        kb.add(InlineKeyboardButton(text=brand, callback_data=brand))
    return kb.adjust(4).as_markup()


async def move_pair(name, brand, i):
    mp = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="left", callback_data=f"left_{brand}_{i}"),
         InlineKeyboardButton(text=name, callback_data=f"{brand}_{name}_{i}"),
         InlineKeyboardButton(text="right", callback_data=f"right_{brand}_{i}")
         ],
        [InlineKeyboardButton(text="back", callback_data=f"back_{brand}")]
    ])
    return mp
