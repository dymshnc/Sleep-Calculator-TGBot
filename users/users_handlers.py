from aiogram.dispatcher.filters import Command
from main import bot, dp
from aiogram.types import Message
from config import admin_id
from users.keyboards import main_menu, back_to_main
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from datetime import date, datetime, timedelta
import json

MAIN_MENU_TEXT = "<b>🗒 Главное меню.</b>\n\n" \
                 "Выберите нужный вам пункт посредством кнопок ниже. Если присутствуют недопонимания с работой бота, " \
                 "ознакомьтесь с <a href=\"https://telegra.ph/Princip-raboty-bota-10-05\">инструкцией пользования</a>."


class GetUp(StatesGroup):
    GA1 = State()


class Sleep(StatesGroup):
    S1 = State()


@dp.message_handler(lambda m: m.chat.id != admin_id, Command("start"))
async def start_join(message: Message):
    if str(message.from_user.id) != str(admin_id):
        with open('users_DB/' + str(message.from_user.id) + '.json', 'w', encoding='utf8') as write_data_file:
            json.dump(json.loads(str(message.from_user)), write_data_file, ensure_ascii=False)
        write_data_file.close()

    await message.answer(text=MAIN_MENU_TEXT, disable_web_page_preview=True, reply_markup=main_menu)


@dp.message_handler(lambda m: m.chat.id != admin_id, text="Когда нужно проснуться ☀️", state=None)
async def take_id(message: Message):
    await message.answer(text="<b>🕔 Введите время в удобном для вас формате:</b>\n\n<code>"
                              "17:50  => 17:50\n"
                              "1420  => 14:20\n"
                              "6 4  => 06:04\n"
                              "9  => 09:00</code>", reply_markup=back_to_main)

    await GetUp.GA1.set()


@dp.message_handler(lambda m: m.chat.id != admin_id, state=GetUp.GA1)
async def search_info(message: Message, state: FSMContext):
    if str(message.text) == '◀️ Вернуться в главное меню':
        await message.answer(text=MAIN_MENU_TEXT, disable_web_page_preview=True, reply_markup=main_menu)
        await state.finish()
    else:
        time = None

        if len(str(message.text)) == 5 and str(message.text)[2] == ':':
            try:
                time = datetime(10, 10, 10, int(str(message.text)[0:2]), int(str(message.text)[3:5]))
            except:
                time = None

        elif len(str(message.text)) == 4 and str(message.text)[1] != ' ' and str(message.text)[2] != ' ':
            try:
                time = datetime(10, 10, 10, int(str(message.text)[0:2]), int(str(message.text)[2:4]))
            except:
                time = None
        elif (len(str(message.text)) == 3 or len(str(message.text)) == 4 or len(str(message.text)) == 5) and (
                str(message.text)[1] == ' ' or str(message.text)[2] == ' '):
            if len(str(message.text)) == 3:
                try:
                    time = datetime(10, 10, 10, int(str(message.text)[0]), int(str(message.text)[2]))
                except:
                    time = None
            elif len(str(message.text)) == 4 and str(message.text)[1] == ' ':
                try:
                    time = datetime(10, 10, 10, int(str(message.text)[0]), int(str(message.text)[2:4]))
                except:
                    time = None
            elif len(str(message.text)) == 5:
                try:
                    time = datetime(10, 10, 10, int(str(message.text)[0:2]), int(str(message.text)[3:5]))
                except:
                    time = None
        elif len(str(message.text)) == 1 or len(str(message.text)) == 2:
            try:
                time = datetime(10, 10, 10, int(str(message.text)[0:2]), 0)
            except:
                time = None

        if time is not None:
            time_to_text = time
            all_times = []
            for i in range(0, 6):
                time -= timedelta(minutes=90)
                all_times.insert(0, time.strftime('%H:%M'))

            await message.answer(
                text=f"☀️ <b>Если вы хотите проснуться в {time_to_text.strftime('%H:%M')}, то нужно лечь спать в:\n\n\n</b>"
                     f"<b><u>{all_times[0]}</u></b> | <i>Длительность сна: 9 часов.</i>\n\n"
                     f"<b><u>{all_times[1]}</u></b> | <i>Длительность сна: 7.5 часа.</i>\n\n"
                     f"<b><u>{all_times[2]}</u></b> | <i>Длительность сна: 6 часов.</i>\n\n"
                     f"<b><u>{all_times[3]}</u></b> | <i>Длительность сна: 4.5 часа.</i>\n\n"
                     f"<b><u>{all_times[4]}</u></b> | <i>Длительность сна: 3 часа.</i>\n\n"
                     f"<b><u>{all_times[5]}</u></b> | <i>Длительность сна: 1.5 часа.</i>\n\n"
                     f"———\n"
                     f"<i>В это время вы фактически УЖЕ должны спать, а НЕ засыпать. Поэтому, обязательно учитывайте "
                     f"время на своё засыпание.</i>",
                reply_markup=main_menu)

            await state.finish()
        else:
            await message.answer(text="Вы ввели время в неправильном формате, попробуйте ещё раз.",
                                 reply_markup=back_to_main)
            await GetUp.GA1.set()


@dp.message_handler(lambda m: m.chat.id != admin_id, text="Когда нужно лечь спать 🛌", state=None)
async def take_id(message: Message):
    await message.answer(text="<b>🕔 Введите время в удобном для вас формате:</b>\n\n<code>"
                              "17:50  => 17:50\n"
                              "1420  => 14:20\n"
                              "6 4  => 06:04\n"
                              "9  => 09:00</code>\n\n"
                              "———\n"
                              "<i>В введённое вами время вы фактически УЖЕ должны спать, а НЕ засыпать. Поэтому, "
                              "обязательно учитывайте время на своё засыпание.</i>",
                         reply_markup=back_to_main)

    await Sleep.S1.set()


@dp.message_handler(lambda m: m.chat.id != admin_id, state=Sleep.S1)
async def search_info(message: Message, state: FSMContext):
    if str(message.text) == '◀️ Вернуться в главное меню':
        await message.answer(text=MAIN_MENU_TEXT, disable_web_page_preview=True, reply_markup=main_menu)
        await state.finish()
    else:
        time = None

        if len(str(message.text)) == 5 and str(message.text)[2] == ':':
            try:
                time = datetime(10, 10, 10, int(str(message.text)[0:2]), int(str(message.text)[3:5]))
            except:
                time = None

        elif len(str(message.text)) == 4 and str(message.text)[1] != ' ' and str(message.text)[2] != ' ':
            try:
                time = datetime(10, 10, 10, int(str(message.text)[0:2]), int(str(message.text)[2:4]))
            except:
                time = None
        elif (len(str(message.text)) == 3 or len(str(message.text)) == 4 or len(str(message.text)) == 5) and (
                str(message.text)[1] == ' ' or str(message.text)[2] == ' '):
            if len(str(message.text)) == 3:
                try:
                    time = datetime(10, 10, 10, int(str(message.text)[0]), int(str(message.text)[2]))
                except:
                    time = None
            elif len(str(message.text)) == 4 and str(message.text)[1] == ' ':
                try:
                    time = datetime(10, 10, 10, int(str(message.text)[0]), int(str(message.text)[2:4]))
                except:
                    time = None
            elif len(str(message.text)) == 5:
                try:
                    time = datetime(10, 10, 10, int(str(message.text)[0:2]), int(str(message.text)[3:5]))
                except:
                    time = None
        elif len(str(message.text)) == 1 or len(str(message.text)) == 2:
            try:
                time = datetime(10, 10, 10, int(str(message.text)[0:2]), 0)
            except:
                time = None
        if time is not None:
            time_to_text = time
            all_times = []
            for i in range(0, 6):
                time += timedelta(minutes=90)
                all_times.append(time.strftime('%H:%M'))

            await message.answer(
                text=f"🛌 <b>Если вы хотите лечь спать в {time_to_text.strftime('%H:%M')}, "
                     f"то нужно проснуться в:\n\n\n</b>"
                     f"<b><u>{all_times[0]}</u></b> | <i>Длительность сна: 1.5 часа.</i>\n\n"
                     f"<b><u>{all_times[1]}</u></b> | <i>Длительность сна: 3 часа.</i>\n\n"
                     f"<b><u>{all_times[2]}</u></b> | <i>Длительность сна: 4.5 часа.</i>\n\n"
                     f"<b><u>{all_times[3]}</u></b> | <i>Длительность сна: 6 часов.</i>\n\n"
                     f"<b><u>{all_times[4]}</u></b> | <i>Длительность сна: 7.5 часов.</i>\n\n"
                     f"<b><u>{all_times[5]}</u></b> | <i>Длительность сна: 9 часов.</i>",
                reply_markup=main_menu)

            await state.finish()
        else:
            await message.answer(text="Вы ввели время в неправильном формате, попробуйте ещё раз.",
                                 reply_markup=back_to_main)
            await Sleep.S1.set()


@dp.message_handler(lambda m: m.chat.id != admin_id, text="◀️ Вернуться в главное меню")
async def take_id(message: Message):
    await message.answer(text=MAIN_MENU_TEXT, disable_web_page_preview=True, reply_markup=main_menu)
