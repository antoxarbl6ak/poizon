from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
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


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("hello, this is our sneakers shop!", reply_markup=kb.start)


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id == admin:
        await message.answer("you opened admin panel", reply_markup=kb.admin)


@router.callback_query(F.data == "info")
async def get_info(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("our store is the best store you ever seen", reply_markup=kb.back_to_start)


@router.callback_query(F.data == "shipment")
async def get_info(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("our shipment is the fastest, cause Usain Bolt is our courier",
                                     reply_markup=kb.back_to_start)


@router.callback_query(F.data == "catalog")
async def get_info(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Choose.brand)
    await callback.message.edit_text("choose the brand",
                                     reply_markup=await kb.catalog_brands(db.sklad))


@router.callback_query(F.data == "back_to_start")
async def get_info(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await cmd_start(callback.message)


@router.callback_query(F.data == "back_to_admin")
async def get_info(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text("you opened admin panel", reply_markup=kb.admin)


@router.callback_query(F.data == "add_pair")
async def add_pair1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AddPair.brand)
    await callback.message.edit_text("brand?", reply_markup=kb.back_to_admin)


@router.callback_query(F.data == "add_pair_wrong")
async def add_pair1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.answer("pair was deleted\nyou opened admin panel", reply_markup=kb.admin)


@router.callback_query(F.data == "add_pair_correct")
async def add_pair1(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    db.add_pair_load(data)
    await callback.message.answer("pair was added\nyou opened admin panel", reply_markup=kb.admin)


@router.callback_query(Choose.brand)
async def choose_pair(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(brand=callback.data)
    await state.set_state(Choose.name)


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
