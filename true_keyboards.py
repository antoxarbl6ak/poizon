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
     InlineKeyboardButton(text="remove pair", callback_data="remove_pair")],
    [InlineKeyboardButton(text="update data", callback_data="deals")]
])

back_to_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="back", callback_data="back_to_admin")]
])

add_pair_ensure = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="correct", callback_data="add_pair_correct"),
     InlineKeyboardButton(text="wrong", callback_data="add_pair_wrong")]
])

sdek_or_prf = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="сдэк", callback_data="sdek"),
     InlineKeyboardButton(text="почта россии", callback_data="prf")]
])

work_deal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="update data", callback_data="update_data"),
     InlineKeyboardButton(text="close the deal", callback_data="close_deal")],
    [InlineKeyboardButton(text="back", callback_data="back_to_admin")]
])

cancel_deal_ensure = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="yes", callback_data="close_deal_yes"),
     InlineKeyboardButton(text="no", callback_data="back_to_admin")]
])

shipment = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="where is my package", callback_data="shipment_where")],
    [InlineKeyboardButton(text="back", callback_data="back_to_start")]
])


async def catalog_brands(brands):
    kb = InlineKeyboardBuilder()
    for brand in brands:
        kb.add(InlineKeyboardButton(text=brand, callback_data=brand))
    return kb.adjust(4).row(InlineKeyboardButton(text="back", callback_data="back_to_start")).as_markup()


async def move_pair(name, brand, i):
    mp = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="left", callback_data=f"left_{brand}_{i}"),
         InlineKeyboardButton(text="buy", callback_data=f"{brand}_{name}_{i}"),
         InlineKeyboardButton(text="right", callback_data=f"right_{brand}_{i}")
         ],
        [InlineKeyboardButton(text="back", callback_data=f"back_{brand}")]
    ])
    return mp


async def get_sizes(sizes, brand, name, i):
    gs = InlineKeyboardBuilder()
    for size in sizes:
        gs.add(InlineKeyboardButton(text=size, callback_data=f"{brand}_{name}_{size}_{i}"))
    return gs.adjust(4).row(InlineKeyboardButton(text="back", callback_data=f"BackToSneakers_{brand}_{i}")).as_markup()


async def back_to_sneakers(brand, i, mode="markup"):
    bts = InlineKeyboardButton(text="back", callback_data=f"BackToSneakers_{brand}_{i}")
    if mode == "markup":
        return InlineKeyboardBuilder().add(bts).as_markup()
    elif mode == "ship":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="сдэк", callback_data="сдэк"),
             InlineKeyboardButton(text="почта россии", callback_data="почта рф")],
            [bts]
        ])


async def choose_pair_ensure(brand, i):
    cpe = InlineKeyboardBuilder()
    cpe.add(InlineKeyboardButton(text="correct", callback_data=f"ChoosePairCorrect_{brand}_{i}"))
    cpe.add(InlineKeyboardButton(text="wrong", callback_data=f"BackToSneakers_{brand}_{i}"))
    return cpe.as_markup()


async def verify_deal(user):
    vd = InlineKeyboardBuilder()
    vd.add(InlineKeyboardButton(text="verify", callback_data=f"verify_{user}"))
    vd.add(InlineKeyboardButton(text="cancel", callback_data=f"cancel_{user}"))
    return vd.as_markup()
