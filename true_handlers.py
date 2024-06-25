from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, BotCommand, BotCommandScopeDefault, BotCommandScopeChat
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
    i = State()
    size = State()
    fio = State()
    phone_number = State()
    shipment = State()
    city = State()
    address = State()
    screen = State()


class Remove(StatesGroup):
    product = State()
    sizes = State()


class Deal(StatesGroup):
    user = State()
    track = State()
    refuse = State()


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
                                     reply_markup=kb.shipment)


@router.callback_query(F.data == "shipment_where")
async def shipment_get_track(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(State("shipment_track"))
    await callback.message.edit_text("send track num of package you wanna track", reply_markup=kb.back_to_start)


@router.message(State("shipment_track"))
async def shipment_data(message: Message, state: FSMContext):
    await state.update_data(track=message.text)
    data = await state.get_data()
    try:
        await message.answer(f'here is what i found:\n{db.deals[data["track"]]["data"]}', reply_markup=kb.back_to_start)
    except KeyError:
        await message.answer("I couldn\'t find deal for this track num", reply_markup=kb.back_to_start)


@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Choose.brand)
    await callback.message.answer("choose the brand",
                                  reply_markup=await kb.catalog_brands(db.sklad))
    await callback.message.delete()


@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await cmd_start(callback.message, state)
    await callback.message.delete()


@router.callback_query(F.data == "back_to_admin")
async def back_to_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text("you opened admin panel", reply_markup=kb.admin)


@router.callback_query(F.data.split('_')[0] == "BackToSneakers")
async def back_to_sneakers(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_")
    i = int(data[2])
    await callback.answer()
    await state.clear()
    await state.update_data(brand=data[1])
    await state.set_state(Choose.name)
    await callback.message.answer_photo(**await db.choose_pair(data[1], i, "photo"),
                                        reply_markup=await kb.move_pair(db.sklad[data[1]][i]["name"],
                                                                        data[1], 0))
    if callback.message.photo:
        await callback.message.delete()


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


@router.callback_query(F.data == "deals")
async def deals(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(State("get_track"))
    await callback.message.edit_text("send track num of deal you wanna work with", reply_markup=kb.back_to_admin)


@router.message(State("get_track"))
async def update_data_track(message: Message, state: FSMContext):
    await state.update_data(track=message.text)
    await message.answer("choose what you wanna do with deal", reply_markup=kb.work_deal)


@router.callback_query(F.data == "update_data")
async def update_data(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(State("new"))
    await callback.message.answer("send new data for this deal", reply_markup=kb.back_to_admin)


@router.message(State("new"))
async def update_data_new(message: Message, state: FSMContext):
    await state.update_data(new=message.text)
    data = await state.get_data()
    try:
        await db.new_data_deal(data["track"], data["new"])
        await message.answer("deal was successfully updated", reply_markup=kb.back_to_admin)
    except KeyError:
        await message.answer("I couldn\'t find deal for this track", reply_markup=kb.back_to_admin)


@router.callback_query(F.data == "close_deal")
async def close_deal(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("are you sure?", reply_markup=kb.cancel_deal_ensure)


@router.callback_query(F.data == "close_deal_yes")
async def close_deal_yes(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    try:
        await db.close_deal(data["track"])
        await callback.message.answer("deal was successfully closed")
        await callback.message.answer("you opened admin panel", reply_markup=kb.admin)
    except KeyError:
        await callback.message.answer("I couldn\'t find deal for this track")
        await callback.message.answer("you opened admin panel", reply_markup=kb.admin)


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


@router.callback_query(Choose.brand)
async def choose_pair(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(brand=callback.data)
    await state.set_state(Choose.name)
    await callback.message.answer_photo(** await db.choose_pair(callback.data, 0, "photo"),
                                        reply_markup=await kb.move_pair(db.sklad[callback.data][0]["name"], callback.data, 0))
    await callback.message.delete()


@router.callback_query(Choose.name)
async def choose_pair_menu(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    if data[0] == "back":
        await state.clear()
        await catalog(callback, state)
    elif data[0] == "left" or data[0] == "right":
        await callback.answer()
        i = int(data[-1])
        if data[0] == "left":
            i = i - 1
        else:
            i = i + 1
        if i == 0:
            pass
        elif i > 0:
            i = i % len(db.sklad[data[1]])
        else:
            i = len(db.sklad[data[1]]) - 1
        await callback.message.edit_media(media=InputMediaPhoto(**await db.choose_pair(data[1], i, "media")),
                                          reply_markup=await kb.move_pair(db.sklad[data[1]][i]["name"], data[1], i))
    else:
        i = int(data[-1])
        await callback.answer()
        await state.update_data(name=data[1])
        await state.set_state(Choose.size)
        await callback.message.edit_caption(caption=f"{callback.message.text}\nchoose size",
                                            reply_markup=await kb.get_sizes(db.sklad[data[0]][i]["sizes"], data[0], data[1], i))


@router.callback_query(Choose.size)
async def choose_pair_size(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    await callback.answer()
    await state.update_data(size=data[2])
    await state.update_data(i=data[3])
    await state.set_state(Choose.fio)
    await callback.message.answer("send your FIO", reply_markup=await kb.back_to_sneakers(data[0], data[3]))
    await callback.message.delete()


@router.message(Choose.fio)
async def choose_pair_fio(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(fio=message.text)
    await state.set_state(Choose.phone_number)
    await message.answer("send your phone number", reply_markup=await kb.back_to_sneakers(data["brand"], data['i']))


@router.message(Choose.phone_number)
async def choose_pair_phone_number(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(phone_number=message.text)
    await state.set_state(Choose.shipment)
    await message.answer("which way you want shipment?",
                         reply_markup=await kb.back_to_sneakers(data["brand"], data['i'], "ship"))


@router.callback_query(Choose.shipment)
async def choose_pair_shipment(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await state.update_data(shipment=callback.data)
    await state.set_state(Choose.city)
    await callback.message.answer("send the city you at",
                                  reply_markup=await kb.back_to_sneakers(data["brand"], data['i']))


@router.message(Choose.city)
async def choose_pair_city(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(city=message.text)
    await state.set_state(Choose.address)
    await message.answer("send address of your post",
                         reply_markup=await kb.back_to_sneakers(data["brand"], data['i']))


@router.message(Choose.address)
async def choose_pair_shipment(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    await message.answer(f"""is this data correct?\n
    brand: {data['brand']}\n
    name: {data['name']}\n
    size: {data['size']}\n
    fio: {data['fio']}\n
    phone number: {data['phone_number']}\n
    shipment: {data['shipment']}\n
    city: {data['city']}\n
    address: {data['address']}""",
                         reply_markup=await kb.choose_pair_ensure(data["brand"], data['i']))


@router.callback_query(F.data.split('_')[0] == "ChoosePairCorrect")
async def choose_pair_correct(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await state.set_state(Choose.screen)
    await callback.message.answer("send us money and screen to proof",
                                  reply_markup=await kb.back_to_sneakers(data["brand"], data['i']))


@router.message(Choose.screen)
async def choose_pair_screen(message: Message, state: FSMContext):
    await state.update_data(screen=message.photo[-1].file_id)
    data = await state.get_data()
    await bot.send_message(admin, f"@{message.from_user.username} bought this? please admin it")
    await bot.send_photo(admin, data["screen"], caption=f"""
brand: {data['brand']}\n
name: {data['name']}\n
size: {data['size']}\n
fio: {data['fio']}\n
phone number: {data['phone_number']}\n
shipment: {data['shipment']}\n
city: {data['city']}\n
address: {data['address']}""",
                         reply_markup=await kb.verify_deal(message.from_user.id))
    await message.answer("we sent your data to verify, you can write us, all contacts are in info:)")
    await state.clear()


@router.callback_query(F.data.split('_')[0] == "verify")
async def choose_pair_verify(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(user=callback.data.split('_')[1])
    await state.set_state(Deal.track)
    data = callback.message.caption.split('\n') + [f"screen: {callback.message.photo[-1].file_id}"]
    data = [d for d in data if d]
    await state.update_data({d.split(': ')[0]: d.split(': ')[1] for d in data})
    await callback.message.answer("please make track to this deal")
    await callback.message.delete()


@router.message(Deal.track)
async def choose_pair_track(message: Message, state: FSMContext):
    await state.update_data(track=message.text)
    data = await state.get_data()
    await message.answer("info about deal and track num sent to customer, you can update states in admin panel")
    await bot.send_message(data["user"], f"your deal was verified!!! track num is {data['track']}\nyou can watch state of your deal in shipment")
    await bot.send_message(data["user"], "hello, this is our sneakers shop!", reply_markup=kb.start)
    await db.add_deal(data)
    await state.clear()


@router.callback_query(F.data.split('_')[0] == "cancel")
async def choose_pair_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(user=callback.data.split('_')[1])
    await state.set_state(Deal.refuse)
    await callback.message.answer("please send the reason of cancel, i will forward this to customer")
    await callback.message.delete()


@router.message(Deal.refuse)
async def choose_pair_refuse(message: Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data["user"], f"admin canceled the deal the reason is:\n{message.text}")
    await state.clear()
