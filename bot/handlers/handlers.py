from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from bson import ObjectId
from os import remove

from bot.config import ADMINS
from bot.misc import send_parse_request, send_pic_to_detector
from bot.dependencies import mongodb
from bot.keyboard import is_human


router = Router()


@router.message(Command(commands=["ozon"]))
async def parse_ozon_article(message: Message, command: CommandObject):
    if message.from_user.id in ADMINS:
        if article := command.args:
            if await send_parse_request(user_id=message.from_user.id, article=article):
                await message.reply("Ошибка парсинга")
        else:
            await message.reply("Нет аргументов")
    else:
        await message.reply("Вы не админ")


@router.message(Command(commands=["wb"]))
async def parse_wb_article(message: Message, command: CommandObject):
    if message.from_user.id in ADMINS:
        if command.args:
            await message.reply("Этот хэндлер пока не прописан")
        else:
            await message.reply("Нет аргументов")
    else:
        await message.reply("Вы не админ")


@router.message(Command(commands=["help"]))
async def help_command(message: Message):
    if message.from_user.id in ADMINS:
        await message.answer(
            """Бот для парсинга фото отзывов товара и определения на фотографиях человека.
Чтобы начать отправьте боту команду `/ozon (артикул товара)`."""
        )



@router.message(Command(commands=["pics"]))
async def any_pic_proove(message: Message):
    obj_id, link = mongodb.get_random_pic()

    await message.answer_photo(photo=link, caption=obj_id, reply_markup=is_human)


@router.message(Command(commands=['stats']))
async def stats_command(message: Message):
    h, nh, pc = mongodb.stats()
    await message.answer(f"Human pic count: {h}\nNo humans pic count: {nh}\nAll pic count: {pc}")


@router.message(F.photo)
async def photo_handler(message: Message):
    file_id = message.photo[-1].file_id

    obj_id = message.caption

    await message.bot.download(
            file=file_id,
            destination="/tmp/data/humans/"+obj_id+".jpeg"
        )

    mod_count = mongodb.set_human(obj_id=ObjectId(obj_id), human=True)

    await message.reply(f"{obj_id} saved, modified count: {mod_count}")

    # file_path = f"/tmp/{file_id}.jpeg"
    # await message.bot.download(file=file_id, destination=file_path)

    # if await send_pic_to_detector(file_path=file_path):
    #     await message.reply("PERSON ☑️")
    # else:
    #     await message.reply("NO PERSON ❌")
    
    # remove(file_path)


@router.callback_query()
async def is_human_callback(callback: CallbackQuery):
    if callback.data == "positive":
        obj_id = callback.message.caption
        res = mongodb.set_human(obj_id=ObjectId(obj_id), human=True)

        obj_id, link = mongodb.get_random_pic()
        await callback.message.answer_photo(photo=link, caption=obj_id, reply_markup=is_human)

        await callback.answer(f"There is human, update {res}")
        await callback.message.bot.download(
            file=callback.message.photo[-1].file_id,
            destination="/tmp/data/humans/"+obj_id+".jpeg"
        )
        await callback.message.delete()
    if callback.data == "negative":
        obj_id = callback.message.caption
        res = mongodb.set_human(obj_id=ObjectId(obj_id), human=False)

        obj_id, link = mongodb.get_random_pic()
        await callback.message.answer_photo(photo=link, caption=obj_id, reply_markup=is_human)

        await callback.answer(f"There is no human, updated {res}")
        await callback.message.bot.download(
            file=callback.message.photo[-1].file_id,
            destination="/tmp/data/no_humans/"+obj_id+".jpeg"
        )
        await callback.message.delete()
    if callback.data == "stop":
        await callback.answer("Stop sending")
        await callback.message.delete()


