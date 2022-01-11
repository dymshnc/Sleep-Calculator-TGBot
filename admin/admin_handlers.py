import json
from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from main import bot, dp
from aiogram.types import Message
from config import admin_id
from admin.keyboards import main_menu, back_to_main
from aiogram.types import ContentTypes
from aiogram.types import InlineKeyboardMarkup
import asyncio
import os


class InfoSearch(StatesGroup):
    I1 = State()


class Mailing(StatesGroup):
    M1 = State()
    M2 = State()


class PersonMailing(StatesGroup):
    PM1 = State()
    PM2 = State()


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Bot active!", reply_markup=main_menu)


@dp.message_handler(Command("start"), chat_id=admin_id)
async def start_join(message: Message):
    await message.answer(text="Добро пожаловать в админ-меню!", reply_markup=main_menu)


@dp.message_handler(text="Активные пользователи", chat_id=admin_id)
async def active_users(message: Message):
    for path, dirs, files in os.walk('users_DB'):
        active_users_count = 0

        for id in files:
            try:
                await bot.send_chat_action(id[:-5], 'typing')
                await asyncio.sleep(0.2)

                active_users_count += 1
            except:
                pass

        await message.answer(text=f"Количество активных пользователей: {active_users_count}", reply_markup=main_menu)


@dp.message_handler(text="Найти информацию о пользователе", state=None, chat_id=admin_id)
async def take_id(message: Message):
    await message.answer(text="Введите ID пользователя.", reply_markup=back_to_main)

    await InfoSearch.I1.set()


@dp.message_handler(state=InfoSearch.I1, chat_id=admin_id)
async def search_info(message: Message, state: FSMContext):
    if str(message.text) == '◀️ Вернуться в главное меню':
        await message.answer(text="Вы вернулись в главное меню.", reply_markup=main_menu)
        await state.finish()
    else:
        for path, dirs, files in os.walk('users_DB'):
            id_is_be_find = False
            for id in files:
                if str(id[:-5]) == str(message.text):
                    with open(f'users_DB/{id}', 'r', encoding='utf8') as read_data_file:
                        try:
                            await message.answer(text='<code>' + str(json.load(read_data_file)) + '</code>',
                                                 reply_markup=main_menu)
                        except:
                            await message.answer(text="Произошла ошибка при получении данных.", reply_markup=main_menu)
                    read_data_file.close()

                    id_is_be_find = True

            if not id_is_be_find:
                await message.answer(text="Такой ID не был найден.", reply_markup=main_menu)

        await state.finish()


@dp.message_handler(text="Общая рассылка", state=None, chat_id=admin_id)
async def add_button(message: Message):
    await message.answer(
        text="<b>Укажите кнопку в формате:</b>\n\n<code>Кнопка - https://example.com/</code>\n\n\nЕсли она не "
             "требуется, укажите \"<b>0</b>\".",
        reply_markup=back_to_main)

    await Mailing.M1.set()


@dp.message_handler(state=Mailing.M1, chat_id=admin_id)
async def add_message(message: Message, state: FSMContext):
    if str(message.text) == '◀️ Вернуться в главное меню':
        await message.answer(text="Вы вернулись в главное меню.", reply_markup=main_menu)
        await state.finish()
    else:
        await state.update_data(answer1=message.text)

        await message.answer(text="Введите сообщение для рассылки.", reply_markup=back_to_main)
        await Mailing.M2.set()


@dp.message_handler(state=Mailing.M2, chat_id=admin_id, content_types=ContentTypes.PHOTO)
async def search_info(message: Message, state: FSMContext):
    if str(message.text) == '◀️ Вернуться в главное меню':
        await message.answer(text="Вы вернулись в главное меню.", reply_markup=main_menu)
        await state.finish()
    else:
        data = await state.get_data()
        button_string = data.get('answer1')

        file_id = message.photo[-1].file_id

        if str(button_string) != '0':
            try:
                button_text = str(button_string).split(' - ')[0]
                button_url = str(button_string).split(' - ')[1]

                button = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardMarkup(text=str(button_text), url=str(button_url))
                        ]
                    ]
                )
            except:
                await message.answer(text="<b>Ошибка в формировании кнопки!</b>", reply_markup=main_menu)

            try:
                for path, dirs, files in os.walk('users_DB'):
                    sends_counter = 0
                    for id in files:
                        try:
                            if str(id[:-5]) != str(admin_id):
                                await bot.send_photo(chat_id=str(id[:-5]), caption=message.caption, photo=file_id,
                                                     reply_markup=button)
                                sends_counter += 1
                        except:
                            pass

                    await message.answer(text="<b>Разосланное сообщение:</b>")
                    await bot.send_photo(chat_id=admin_id, caption=message.caption, photo=file_id, reply_markup=button)
                    await message.answer(text=f"<b>Успешно отправлено: </b>{sends_counter}.", reply_markup=main_menu)
            except:
                await message.answer(text="<b>Ошибка в рассылке!</b>", reply_markup=main_menu)

            await state.finish()
        else:
            try:
                for path, dirs, files in os.walk('users_DB'):
                    sends_counter = 0
                    for id in files:
                        try:
                            if str(id[:-5]) != str(admin_id):
                                await bot.send_photo(chat_id=str(id[:-5]), caption=message.caption, photo=file_id)
                                sends_counter += 1
                        except:
                            pass

                    await message.answer(text="<b>Разосланное сообщение:</b>")
                    await bot.send_photo(chat_id=admin_id, caption=message.caption, photo=file_id,
                                         reply_markup=main_menu)
                    await message.answer(text=f"<b>Успешно отправлено: </b>{sends_counter}.", reply_markup=main_menu)
            except:
                await message.answer(text="<b>Ошибка в рассылке!</b>", reply_markup=main_menu)

            await state.finish()


@dp.message_handler(state=Mailing.M2, chat_id=admin_id, content_types=ContentTypes.ANIMATION)
async def search_info(message: Message, state: FSMContext):
    if str(message.text) == '◀️ Вернуться в главное меню':
        await message.answer(text="Вы вернулись в главное меню.", reply_markup=main_menu)
        await state.finish()
    else:
        data = await state.get_data()
        button_string = data.get('answer1')

        file_id = message.animation.file_id

        if str(button_string) != '0':
            try:
                button_text = str(button_string).split(' - ')[0]
                button_url = str(button_string).split(' - ')[1]

                button = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardMarkup(text=str(button_text), url=str(button_url))
                        ]
                    ]
                )
            except:
                await message.answer(text="<b>Ошибка в формировании кнопки!</b>", reply_markup=main_menu)

            try:
                for path, dirs, files in os.walk('users_DB'):
                    sends_counter = 0
                    for id in files:
                        try:
                            if str(id[:-5]) != str(admin_id):
                                await bot.send_animation(chat_id=str(id[:-5]), caption=message.caption,
                                                         animation=file_id,
                                                         reply_markup=button)
                                sends_counter += 1
                        except:
                            pass

                    await message.answer(text="<b>Разосланное сообщение:</b>")
                    await bot.send_animation(chat_id=admin_id, caption=message.caption, animation=file_id,
                                             reply_markup=button)
                    await message.answer(text=f"<b>Успешно отправлено: </b>{sends_counter}.", reply_markup=main_menu)
            except:
                await message.answer(text="<b>Ошибка в рассылке!</b>", reply_markup=main_menu)

            await state.finish()
        else:
            try:
                for path, dirs, files in os.walk('users_DB'):
                    sends_counter = 0
                    for id in files:
                        try:
                            if str(id[:-5]) != str(admin_id):
                                await bot.send_animation(chat_id=str(id[:-5]), caption=message.caption,
                                                         animation=file_id)
                                sends_counter += 1
                        except:
                            pass

                    await message.answer(text="<b>Разосланное сообщение:</b>")
                    await bot.send_animation(chat_id=admin_id, caption=message.caption, animation=file_id,
                                             reply_markup=main_menu)
                    await message.answer(text=f"<b>Успешно отправлено: </b>{sends_counter}.", reply_markup=main_menu)
            except:
                await message.answer(text="<b>Ошибка в рассылке!</b>", reply_markup=main_menu)

            await state.finish()


@dp.message_handler(state=Mailing.M2, chat_id=admin_id)
async def search_info(message: Message, state: FSMContext):
    if str(message.text) == '◀️ Вернуться в главное меню':
        await message.answer(text="Вы вернулись в главное меню.", reply_markup=main_menu)
        await state.finish()
    else:
        data = await state.get_data()
        button_string = data.get('answer1')

        if str(button_string) != '0':
            try:
                button_text = str(button_string).split(' - ')[0]
                button_url = str(button_string).split(' - ')[1]

                button = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardMarkup(text=str(button_text), url=str(button_url))
                        ]
                    ]
                )
            except:
                await message.answer(text="<b>Ошибка в формировании кнопки!</b>", reply_markup=main_menu)
            try:
                for path, dirs, files in os.walk('users_DB'):
                    sends_counter = 0

                    for id in files:
                        try:
                            if str(id[:-5]) != str(admin_id):
                                await bot.send_message(chat_id=str(id[:-5]), text=str(message.text),
                                                       reply_markup=button)
                                sends_counter += 1
                        except:
                            pass

                    await message.answer(text=f"<b>Разосланное сообщение:</b>\n\n{message.text}",
                                         reply_markup=button)
                    await message.answer(text=f"<b>Успешно отправлено: </b>{sends_counter}.", reply_markup=main_menu)
            except:
                await message.answer(text="<b>Ошибка в рассылке!</b>", reply_markup=main_menu)

            await state.finish()
        else:
            try:
                for path, dirs, files in os.walk('users_DB'):
                    sends_counter = 0

                    for id in files:
                        try:
                            if str(id[:-5]) != str(admin_id):
                                await bot.send_message(chat_id=str(id[:-5]), text=str(message.text))
                                sends_counter += 1
                        except:
                            pass

                    await message.answer(text=f"<b>Разосланное сообщение:</b>\n\n{message.text}",
                                         reply_markup=main_menu)
                    await message.answer(text=f"<b>Успешно отправлено: </b>{sends_counter}.", reply_markup=main_menu)
            except:
                await message.answer(text="<b>Ошибка в рассылке!</b>", reply_markup=main_menu)

            await state.finish()


@dp.message_handler(text="Личное сообщение", state=None, chat_id=admin_id)
async def take_id(message: Message):
    await message.answer(text="Введите сообщение для рассылки.", reply_markup=back_to_main)

    await PersonMailing.PM1.set()


@dp.message_handler(state=PersonMailing.PM1, chat_id=admin_id)
async def search_info(message: Message, state: FSMContext):
    if str(message.text) == '◀️ Вернуться в главное меню':
        await message.answer(text="Вы вернулись в главное меню.", reply_markup=main_menu)
        await state.finish()
    else:
        await state.update_data(answer1=message.text)

        await message.answer(text="Введите ID пользователя.", reply_markup=back_to_main)

        await PersonMailing.PM2.set()


@dp.message_handler(state=PersonMailing.PM2, chat_id=admin_id)
async def search_info(message: Message, state: FSMContext):
    if str(message.text) == '◀️ Вернуться в главное меню':
        await message.answer(text="Вы вернулись в главное меню.", reply_markup=main_menu)
        await state.finish()
    else:
        data = await state.get_data()
        mail = data.get('answer1')
        usr_id = message.text

        for path, dirs, files in os.walk('users_DB'):
            temp_key = False

            for id in files:
                if str(id[:-5]) == str(usr_id):
                    try:
                        await bot.send_message(chat_id=str(id[:-5]), text=str(mail))
                        temp_key = True
                        break
                    except:
                        await message.answer(text="Произошла ошибка при отправке сообщения.", reply_markup=main_menu)

            if temp_key:
                await message.answer(text=f"<b>Отправленное сообщение:</b>\n\n{mail}", reply_markup=main_menu)
            else:
                await message.answer(text="Такой ID не был найден.", reply_markup=main_menu)

        await state.finish()


@dp.message_handler(text="◀️ Вернуться в главное меню", chat_id=admin_id)
async def take_id(message: Message):
    await message.answer(text="Вы вернулись в главное меню.", reply_markup=main_menu)
