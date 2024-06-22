from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from os import getenv
from dotenv import load_dotenv
import true_keyboards as kb
import db


load_dotenv()
bot = Bot(getenv("TOKEN"))

router = Router()

with open("admin.txt") as a:
    admin = int(a.readline())


class AddPair(StatesGroup):
    brand = State()
    name = State()
    photo = State()
    price = State()
    sizes = State()


class Choose(StatesGroup):
    brand = State()
    name = State()


class Remove(StatesGroup):
    product = State()
    sizes = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("hello, this is our sneakers shop!", reply_markup=kb.start)


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    if message.from_user.id == admin:
        await state.clear()
        await message.answer("you opened admin panel", reply_markup=kb.admin)


@router.callback_query(F.data == "info")
async def get_info(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("our store is the best store you ever seen", reply_markup=kb.back_to_start)


@router.callback_query(F.data == "shipment")
async def shipment(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("our shipment is the fastest, cause Usain Bolt is our courier",
                                     reply_markup=kb.back_to_start)


@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Choose.brand)
    await callback.message.answer("choose the brand",
                                  reply_markup=await kb.catalog_brands(db.sklad))


@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await cmd_start(callback.message)


@router.callback_query(F.data == "back_to_admin")
async def back_to_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text("you opened admin panel", reply_markup=kb.admin)


@router.callback_query(F.data == "add_pair")
async def add_pair1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AddPair.brand)
    await callback.message.edit_text("brand?", reply_markup=kb.back_to_admin)


@router.callback_query(F.data == "add_pair_wrong")
async def add_pair2(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.answer("pair was deleted\nyou opened admin panel", reply_markup=kb.admin)


@router.callback_query(F.data == "add_pair_correct")
async def add_pair3(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await db.add_pair_load(data)
    await callback.message.answer("pair was added\nyou opened admin panel", reply_markup=kb.admin)


@router.callback_query(F.data == "remove_pair")
async def remove_pair_request(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Remove.product)
    await callback.message.edit_text("send name of pair as in catalog")


@router.message(Remove.product)
async def remove_pair_choose(message: Message, state: FSMContext):
    await state.update_data(product=message.text)
    await state.set_state(Remove.sizes)
    await message.answer("if you want remove all sizes send: all\nelse send all sizes you want to remove: 36 37 39")


@router.message(Remove.sizes)
async def remove_pair_actually(message: Message, state: FSMContext):
    await state.update_data(sizes=message.text)
    await message.answer(await db.remove_pair(**await state.get_data()))
    await state.clear()
    await message.answer("you opened admin panel", reply_markup=kb.admin)


@router.callback_query(Choose.brand)
async def choose_pair(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(brand=callback.data)
    await state.set_state(Choose.name)
    await callback.message.answer_photo(** await db.choose_pair(callback.data, 0, "photo"),
                                        reply_markup=await kb.move_pair(db.sklad[callback.data][0]["name"], callback.data, 0))


@router.callback_query(Choose.name)
async def choose_pair_menu(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    i = data[-1]
    if data[0] == "back":
        await state.clear()
        await catalog(callback, state)
    elif data[0] == "left" or data[0] == "right":
        await callback.answer()
        if data[0] == "left":
            i = int(i) - 1
        else:
            i = int(i) + 1
        if i == 0:
            pass
        elif i > 0:
            i = i % len(db.sklad[data[1]])
        else:
            i = len(db.sklad[data[1]]) - 1
        await callback.message.edit_media(media=InputMediaPhoto(**await db.choose_pair(data[1], i, "media")),
                                          reply_markup=await kb.move_pair(db.sklad[data[1]][i]["name"], data[1], i))
    else:
        pass


@router.message(AddPair.brand)
async def add_pair2(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await state.set_state(AddPair.name)
    await message.answer("name?", reply_markup=kb.back_to_admin)


@router.message(AddPair.name)
async def add_pair2(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddPair.photo)
    await message.answer("photo?", reply_markup=kb.back_to_admin)


@router.message(AddPair.photo)
async def add_pair2(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(AddPair.price)
    await message.answer("price?", reply_markup=kb.back_to_admin)


@router.message(AddPair.price)
async def add_pair2(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(AddPair.sizes)
    await message.answer("sizes in EU?", reply_markup=kb.back_to_admin)


@router.message(AddPair.sizes)
async def add_pair2(message: Message, state: FSMContext):
    await state.update_data(sizes=message.text.split())
    data = await state.get_data()
    await message.answer_photo(photo=data["photo"],
                               caption=f"{data['brand']}\n{data['name']}: {data['price']}\nsizes in stock: {' '.join(data['sizes'])}",
                               reply_markup=kb.add_pair_ensure)
