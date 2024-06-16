import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType

import config
import keyboard as kb
import tester
from datab import Database
from geocode import get_ll_span

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

# создание бота и его состояний
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)
db = Database("hospital.db")


class AllStates(StatesGroup):
    name = State()
    admin_name = State()
    admin_password = State()

    delete_user = State()

    obl_add = State()

    gor_add = State()
    gor1_add = State()
    gor_end = State()

    hos_add = State()
    hos1_add = State()
    hos2_add = State()
    hos3_add = State()
    hos_end = State()

    doc_add = State()
    doc1_add = State()
    doc2_add = State()
    doc3_add = State()
    doc_end = State()

    doc_del = State()
    doc1_del = State()
    docdel_end = State()

    gl_q1 = State()
    gl_q2 = State()
    gl_q3 = State()
    gl_q4 = State()
    gl_q5 = State()
    gl_answ = State()

    zh_q1 = State()
    zh_q2 = State()
    zh_q3 = State()
    zh_q4 = State()
    zh_q5 = State()
    zh_answ = State()

    zub_q1 = State()
    zub_q2 = State()
    zub_q3 = State()
    zub_q4 = State()
    zub_q5 = State()
    zub_answ = State()

    ru_q1 = State()
    ru_q2 = State()
    ru_q3 = State()
    ru_q4 = State()
    ru_q5 = State()
    ru_answ = State()

    uh_q1 = State()
    uh_q2 = State()
    uh_q3 = State()
    uh_q4 = State()
    uh_q5 = State()
    uh_answ = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if not db.user_exists(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Здравствуйте! Как мне к вам обращаться?")
        await AllStates.name.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Здравствуйте, {db.get_name(message.from_user.id)}",
                               reply_markup=kb.menu)


@dp.message_handler(state=AllStates.name)
async def set_name(message: types.Message, state: FSMContext):
    if message.text.isalpha() and not message.text.isdigit():
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Приятно познакомиться, {message.text}!")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Я медицинский чат-бот, отправь /help и узнай, как мной можно пользоваться :)",
                               reply_markup=kb.menu)
        await state.finish()
        db.add_user(message.from_user.id, message.text)

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отправьте пожалуйста имя текстом")


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=config.HELP_MES)


@dp.message_handler(text=['🏠 Личный кабинет'])
async def lk(message: types.Message):
    if db.get_photo(message.from_user.id):
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=db.get_photo(message.from_user.id))
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Ваше имя - {db.get_name(message.from_user.id)}",
                           reply_markup=kb.lk_menu)


@dp.message_handler(text=['Панель администратора'])
async def admin(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите имя администратора",
                           reply_markup=kb.admin_registr)
    await AllStates.admin_name.set()


@dp.message_handler(state=AllStates.admin_name)
async def admin_name(message: types.Message, state: FSMContext):
    if message.text == db.get_admin_name():
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите пароль администратора",
                               reply_markup=kb.admin_registr)
        await state.finish()
        await AllStates.admin_password.set()
    elif message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена входа в панель администратора",
                               reply_markup=kb.menu)
        await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите имя администратора",
                               reply_markup=kb.admin_registr)


@dp.message_handler(state=AllStates.admin_password)
async def admin_password(message: types.Message, state: FSMContext):
    if message.text == db.get_admin_password():
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы вошли в панель администратора",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена входа в панель администратора",
                               reply_markup=kb.menu)
        await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите пароль администратора",
                               reply_markup=kb.admin_registr)


@dp.message_handler(text=['Добавить город'])
async def edit_areas(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите название города",
                           reply_markup=kb.admin_cancel)
    await AllStates.gor_add.set()


@dp.message_handler(state=AllStates.gor_add)
async def add_gor(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена добавления города",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.check_good(message.text):
        async with state.proxy() as data:
            data['gor'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Напишите область, в которой находится город",
                               reply_markup=kb.cancel)
        await AllStates.next()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректное название",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(state=AllStates.gor1_add)
async def add_gor1(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена добавления города",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.check_good(message.text):
        async with state.proxy() as data:
            data['obl'] = message.text
        await AllStates.next()
        async with state.proxy() as data:
            if db.check(data['obl']):
                db.add_gor(data['gor'], data['obl'])
            else:
                db.create_obl(data['obl'])
                db.add_gor(data['gor'], data['obl'])
            db.create_gor(data['gor'])
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Город '{data['gor']}' добавлен в {data['obl']}",
                                   reply_markup=kb.admin_menu)
        await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректное название",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(text=['Добавить больницу'])
async def edit_areas(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите название больницы",
                           reply_markup=kb.admin_cancel)
    await AllStates.hos_add.set()


@dp.message_handler(state=AllStates.hos_add)
async def add_hos(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена добавления больницы",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.check_good(message.text):
        async with state.proxy() as data:
            data['hos'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Напишите город, в которой находится больница",
                               reply_markup=kb.cancel)
        await AllStates.next()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректное название",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(state=AllStates.hos1_add)
async def add_hos1(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена добавления больницы",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.check_good(message.text):
        async with state.proxy() as data:
            data['gor'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Напишите контактный номер больницы\n"
                                    f"Пример: +7 (47461) 3-75-65",
                               reply_markup=kb.cancel)
        await AllStates.next()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректное название",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(state=AllStates.hos2_add)
async def add_hos2(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена добавления больницы",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.validate_phone_number(message.text):
        async with state.proxy() as data:
            data['num'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Напишите адрес больницы\n"
                                    f"Пример: Липецкая область, Грязи, Социалистическая улица, 5",
                               reply_markup=kb.cancel)
        await AllStates.next()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректный номер",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(state=AllStates.hos3_add)
async def add_hos3(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена добавления больницы",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif message.text:
        async with state.proxy() as data:
            data['adr'] = message.text
        await AllStates.next()
        async with state.proxy() as data:
            if db.check(data['gor']):
                db.create_hospital(data['hos'])
                db.add_hos(data['hos'], data['gor'], data['adr'], data['num'])
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Больница '{data['hos']}' добавлена в {data['gor']}",
                                       reply_markup=kb.admin_menu)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Для начала добавьте такой город, как {data['gor']}",
                                       reply_markup=kb.admin_menu)
        await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректный адрес",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(text=['Редактировать врачей'])
async def edit_docs(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите действие:",
                           reply_markup=kb.doc_menu)


@dp.callback_query_handler(lambda message: message.data == "deldoc")
async def del_doc(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Введите название больницы",
                           reply_markup=kb.admin_cancel)
    await AllStates.doc_del.set()


@dp.message_handler(state=AllStates.doc_del)
async def del_doc1(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена удаления врача",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.check_good(message.text):
        async with state.proxy() as data:
            data['hos'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Напишите имя врача",
                               reply_markup=kb.cancel)
        await AllStates.next()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректное название",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(state=AllStates.doc1_del)
async def del_doc2(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена удаления врача",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.check_good(message.text):
        async with state.proxy() as data:
            data['nam'] = message.text
        await AllStates.next()
        async with state.proxy() as data:
            db.del_doc(data['nam'], data['hos'])
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Врач '{data['nam']}' удален из больницы '{data['hos']}'",
                                   reply_markup=kb.admin_menu)
            await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректное имя",
                               reply_markup=kb.admin_cancel)


@dp.callback_query_handler(lambda message: message.data == "adddoc")
async def bot_adddoc(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Введите название больницы",
                           reply_markup=kb.admin_cancel)
    await AllStates.doc_add.set()


@dp.message_handler(state=AllStates.doc_add)
async def add_doc(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена добавления врача",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.check_good(message.text):
        async with state.proxy() as data:
            data['hos'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Напишите имя врача",
                               reply_markup=kb.cancel)
        await AllStates.next()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректное название",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(state=AllStates.doc1_add)
async def add_doc1(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена добавления врача",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.check_good(message.text):
        async with state.proxy() as data:
            data['nam'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Напишите должность врача\n"
                                    f"Пример: Стоматолог",
                               reply_markup=kb.cancel)
        await AllStates.next()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректное имя",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(state=AllStates.doc2_add)
async def add_doc2(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена добавления врача",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.check_good(message.text):
        async with state.proxy() as data:
            data['who'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Напишите кабинет врача\n"
                                    f"Пример: 325",
                               reply_markup=kb.cancel)
        await AllStates.next()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректную должность",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(state=AllStates.doc3_add)
async def add_doc3(message: types.Message, state: AllStates):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена добавления врача",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif message.text:
        async with state.proxy() as data:
            data['cab'] = message.text
        await AllStates.next()
        async with state.proxy() as data:
            if db.check(data['hos'], True):
                db.add_doc(data['nam'], data['who'], data['hos'], data['cab'])
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Врач '{data['nam']}' добавлен в {data['hos']}",
                                       reply_markup=kb.admin_menu)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Для начала добавьте такую больницу, как {data['hos']}",
                                       reply_markup=kb.admin_menu)
        await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректный кабинет",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(text=['Добавить область'])
async def edit_areas(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите название области",
                           reply_markup=kb.admin_cancel)
    await AllStates.obl_add.set()


@dp.message_handler(state=AllStates.obl_add)
async def add_obl(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена добавления области",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.check_good(message.text):
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Вы создали таблицу '{message.text}'",
                               reply_markup=kb.admin_menu)
        db.create_obl(message.text)
        await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите корректное название",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(text=['Удалить пользователя'])
async def del_user(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите id пользователя, которого хотите удалить",
                           reply_markup=kb.admin_cancel)
    await AllStates.delete_user.set()


@dp.message_handler(state=AllStates.delete_user)
async def delete_user(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отмена удаления",
                               reply_markup=kb.admin_menu)
        await state.finish()
    elif tester.check_user(message.text):
        db.delete_user(message.text)
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Вы удалили пользователя с id - {message.text}",
                               reply_markup=kb.admin_menu)
        await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Пользователь не найден",
                               reply_markup=kb.admin_cancel)


@dp.message_handler(text=['В главное меню'])
async def admin_back(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы вернулись в главное меню",
                           reply_markup=kb.menu)


@dp.message_handler(text=['⬅ Назад'])
async def back(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы вернулись в главное меню",
                           reply_markup=kb.menu)


@dp.message_handler(text=['📋 Записаться к врачу'])
async def doctor(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Для записи к врачу перейдите по ссылке:",
                           reply_markup=kb.doctor)


@dp.message_handler(text=['❤ Симптомы'])
async def docs(message: types.Message, state: FSMContext):
    await message.answer(text="Что у Вас болит?",
                         reply_markup=kb.menu_simp)
    await state.finish()


# ГОЛОВА
@dp.message_handler(text=['🧠 Голова'])
async def g1_st(message: types.Message):
    await message.answer(text="Ответьте на несоклько вопросов")
    await AllStates.gl_q1.set()
    await message.answer(text="Как давно болит голова?<b>\nДавно/Недавно/Не знаю</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.gl_q1)
async def g1_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_1'] = message.text
    await AllStates.next()
    await message.answer(text="Может быть вы упали? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.gl_q2)
async def g2_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_2'] = message.text
    await AllStates.next()
    await message.answer(text="Мерили давление? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.gl_q3)
async def g3_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_3'] = message.text
    await AllStates.next()
    await message.answer(text="Вы уже приняли лекарство? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.gl_q4)
async def g4_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_4'] = message.text
    await AllStates.next()
    await message.answer(text="У вас сильно болит голова? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.gl_q5)
async def g5_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_5'] = message.text
    await AllStates.next()

    async with state.proxy() as data:
        # ответ на результаты исследования при выборе головы
        if data['1_1'] == "Давно" and data['1_2'] == "Да" and data['1_3'] == "Нет" \
                and data['1_4'] == "Да" and data['1_5'] == "Да":
            await message.answer(text="Видимо у вас мигрень, обратитесь к врачу, ссылка для записи ниже",
                                 reply_markup=kb.inline_kb1)

        elif data['1_1'] == "Недавно" and data['1_2'] == "Нет" and data['1_3'] == "Нет" \
                and data['1_4'] == "Нет" and data['1_5'] == "Да":
            await message.answer(
                text="Видимо у вас просто болит голова, выпейте лекарство или запишитесь к врачу на обследдование",
                reply_markup=kb.inline_kb1)

        elif data['1_1'] == "Давно" and data['1_2'] == "Нет" and data['1_3'] == "Нет" \
                and data['1_4'] == "Нет" and data['1_5'] == "Да":
            await message.answer(
                text="Видимо у вас просто болит голова, выпейте лекарство или запишитесь к врачу на обследдование",
                reply_markup=kb.inline_kb1)

        elif data['1_1'] == "Не знаю" and data['1_2'] == "Нет" and data['1_3'] == "Да" \
                and data['1_4'] == "Нет" and data['1_5'] == "Да":
            await message.answer(
                text="Видимо вы сильно упали, советуем записаться к врачу на диагностику головы",
                reply_markup=kb.inline_kb1)

        elif (data['1_1'] == "Нет" or data['1_1'] == "Не знаю") and data['1_2'] == "Нет" and data['1_3'] == "Нет" \
                and data['1_4'] == "Нет" and data['1_5'] == "Нет":
            await message.answer(text="Может у вас ничего не болит?", reply_markup=kb.inline_kb1)

        else:
            await message.answer(text="Советуем выпить лекарства и подождать,"
                                      " если не помогло - вернитесь назад и нажмите на кнопку 📋 Записаться к врачу")

    await state.finish()


# ЖИВОТ
@dp.message_handler(text=['❤ Живот'])
async def zh1_st(message: types.Message):
    await message.answer(text="Ответьте на несоклько вопросов")
    await AllStates.zh_q1.set()
    await message.answer(text="Как давно болит живот? <b>\nДавно/Недавно/Не знаю</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.zh_q1)
async def zh1_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_1'] = message.text
    await AllStates.next()
    await message.answer(text="Может быть вы ушиблись? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.zh_q2)
async def zh2_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_2'] = message.text
    await AllStates.next()
    await message.answer(text="У вас есть темпреатура? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.zh_q3)
async def zh3_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_3'] = message.text
    await AllStates.next()
    await message.answer(text="Вы уже приняли лекарство? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.zh_q4)
async def zh4_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_4'] = message.text
    await AllStates.next()
    await message.answer(text="У вас сильно болит живот? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.zh_q5)
async def zh5_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_5'] = message.text
    await AllStates.next()

    async with state.proxy() as data:
        # ответ на результаты исследования при выборе головы
        if data['1_1'] == "Давно" and data['1_2'] == "Нет" and data['1_3'] == "Нет" \
                and data['1_4'] == "Да" and data['1_5'] == "Да":
            await message.answer(
                text="Видимо у вас несварение, если это продолжиться то обратитесь к врачу, ссылка для записи ниже",
                reply_markup=kb.inline_kb1)

        elif data['1_1'] == "Недавно" and data['1_2'] == "Нет" and data['1_3'] == "Да" \
                and data['1_4'] == "Нет" and data['1_5'] == "Да":
            await message.answer(
                text="Скорее выпейте лекарство или запишитесь к врачу на обследование",
                reply_markup=kb.inline_kb1)

        elif data['1_1'] == "Давно" and data['1_2'] == "Нет" and data['1_3'] == "Нет" \
                and data['1_4'] == "Нет" and data['1_5'] == "Да":
            await message.answer(
                text="Видимо у вас просто болит живот, выпейте лекарство или запишитесь к врачу на обследдование",
                reply_markup=kb.inline_kb1)

        elif data['1_1'] == "Не знаю" and data['1_2'] == "Нет" and data['1_3'] == "Да" \
                and data['1_4'] == "Нет" and data['1_5'] == "Да":
            await message.answer(
                text="Видимо вы просто ударились, советуем записаться к врачу на диагностику живота",
                reply_markup=kb.inline_kb1)

        elif (data['1_1'] == "Нет" or data['1_1'] == "Не знаю") and data['1_2'] == "Нет" and data['1_3'] == "Нет" \
                and data['1_4'] == "Нет" and data['1_5'] == "Нет":
            await message.answer(text="Может у вас ничего не болит?", reply_markup=kb.inline_kb1)

        else:
            await message.answer(text="Советуем выпить лекарства и подождать,"
                                      " если не помогло - вернитесь назад и нажмите на кнопку 📋 Записаться к врачу")

    await state.finish()


# ЗУБ
@dp.message_handler(text=['🦷 Зубы'])
async def z_st(message: types.Message):
    await message.answer(text="Ответьте на несоклько вопросов")
    await AllStates.zub_q1.set()
    await message.answer(text="Как давно у вас болят зубы? <b>\nДавно/Недавно/Не знаю</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.zub_q1)
async def z1_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_1'] = message.text
    await AllStates.next()
    await message.answer(text="Могли ли произойти скол кусочка зуба? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.zub_q2)
async def z2_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_2'] = message.text
    await AllStates.next()
    await message.answer(text="Чистите ли вы зубы 2 раза в день? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.zub_q3)
async def z3_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_3'] = message.text
    await AllStates.next()
    await message.answer(text="Вы уже выпили лекарство? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.zub_q4)
async def z4_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_4'] = message.text
    await AllStates.next()
    await message.answer(text="Ели ли вы кислое/фрукты недавно? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.zub_q5)
async def z5_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_5'] = message.text
    await AllStates.next()

    async with state.proxy() as data:
        # ответ на результаты исследования при выборе головы
        if data['1_1'] == "Недавно" and data['1_2'] == "Нет" and data['1_3'] == "Да" \
                and data['1_4'] == "Да" and data['1_5'] == "Да":
            await message.answer(text="Возможно зуб болит из-за принятой пищи, прополощите рот, если боль не утихнет"
                                      " то запишитесь к стоматологу по кнопке внизу", reply_markup=kb.inline_kb1)

        elif data['1_1'] == "Недавно" and data['1_2'] == "Нет" and data['1_3'] == "Да" \
                and data['1_4'] == "Нет" and data['1_5'] == "Да":
            await message.answer(
                text="Возможно зуб болит из-за принятой пищи, прополощите рот и можете выпить слабое обезболивающие,"
                     " если боль не утихнет то запишитесь к стоматологу по кнопке внизу", reply_markup=kb.inline_kb1)

        elif (data['1_1'] == "Давно" or data['1_1'] == "Не знаю") and data['1_2'] == "Нет" and data['1_3'] == "Нет" \
                and data['1_4'] == "Да" and data['1_5'] == "Нет":
            await message.answer(
                text="У вас может быть повреждена эмаль зубов, обратитесь к стоматологу по кнопке снизу",
                reply_markup=kb.inline_kb1)

        elif (data['1_1'] == "Не знаю" or data['1_1'] == 'Недавно') and data['1_2'] == "Да" and data['1_3'] == "Да" \
                and data['1_4'] == "Нет" and data['1_5'] == "Нет":
            await message.answer(
                text="Видимо вы скололи небольшой кусочек зуба, советуем записаться к стоматологу",
                reply_markup=kb.inline_kb1)

        elif (data['1_1'] == "Нет" or data['1_1'] == "Не знаю") and data['1_2'] == "Нет" and data['1_3'] == "Нет" \
                and data['1_4'] == "Нет" and data['1_5'] == "Нет":
            await message.answer(text="Может у вас ничего не болит?", reply_markup=kb.inline_kb1)

        else:
            await message.answer(text="Советуем выпить лекарства и подождать,"
                                      " если не помогло - вернитесь назад и нажмите на кнопку 📋 Записаться к врачу")

    await state.finish()


# РУКА ИЛИ НОГА
@dp.message_handler(text=['💪 Рука или нога'])
async def r1_st(message: types.Message):
    await message.answer(text="Ответьте на несоклько вопросов")
    await AllStates.ru_q1.set()
    await message.answer(text="Как давно у вас болит конечность? <b>\nДавно/Недавно/Не знаю</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.ru_q1)
async def r1_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_1'] = message.text
    await AllStates.next()
    await message.answer(text="Может вы ушиблись? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.ru_q2)
async def r2_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_2'] = message.text
    await AllStates.next()
    await message.answer(text="У вас есть синяк на конечности? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.ru_q3)
async def r3_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_3'] = message.text
    await AllStates.next()
    await message.answer(text="Вас мог кто-то укусить? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.ru_q4)
async def r4_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_4'] = message.text
    await AllStates.next()
    await message.answer(text="Сильно ли болит конечность? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.ru_q5)
async def r5_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_5'] = message.text
    await AllStates.next()

    async with state.proxy() as data:
        # ответ на результаты исследования при выборе головы
        if (data['1_1'] == "Недавно" or data['1_1'] == "Не знаю") and data['1_2'] == "Нет" and data['1_3'] == "Да" \
                and data['1_4'] == "Да" and data['1_5'] == "Да":
            await message.answer(
                text="Возможно вас укусило какое-либо насекомое или животное, советуем обратиться к врачу",
                reply_markup=kb.inline_kb1)

        elif (data['1_1'] == "Недавно" or data['1_1'] == "Не знаю") and data['1_2'] == "Нет" and data['1_3'] == "Да" \
                and data['1_4'] == "Нет" and data['1_5'] == "Нет":
            await message.answer(
                text="Возмона нехватка воды в организме, если это будет причинять дискомфорт, то обратитесь к врачу",
                reply_markup=kb.inline_kb1)

        elif (data['1_1'] == "Давно" or data['1_1'] == "Не знаю") and data['1_2'] == "Да" and data['1_3'] == "Да" \
                and data['1_4'] == "Нет" and data['1_5'] == "Да":
            await message.answer(
                text="Скорее всего вы сильно ударились, рекомендуем обратится к травматологу",
                reply_markup=kb.inline_kb1)

        elif (data['1_1'] == "Не знаю" or data['1_1'] == 'Недавно') and data['1_2'] == "Да" and data['1_3'] == "Да" \
                and data['1_4'] == "Нет" and data['1_5'] == "Нет":
            await message.answer(
                text="Возможно вы не сильно ударились, через некоторое время пройдет")

        elif (data['1_1'] == "Нет" or data['1_1'] == "Не знаю") and data['1_2'] == "Нет" and data['1_3'] == "Нет" \
                and data['1_4'] == "Нет" and data['1_5'] == "Нет":
            await message.answer(text="Может у вас ничего не болит?", reply_markup=kb.inline_kb1)

        else:
            await message.answer(text="Советуем выпить обезболивающее и подождать, если не помогло - вернитесь"
                                      " назад и нажмите на кнопку 📋 Записаться к врачу")

    await state.finish()


# УХО
@dp.message_handler(text=['👂 Ухо'])
async def u1_st(message: types.Message):
    await message.answer(text="Ответьте на несоклько вопросов")
    await AllStates.uh_q1.set()
    await message.answer(text="Как давно у вас болит ухо? <b>\nДавно/Недавно/Не знаю</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.uh_q1)
async def u1_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_1'] = message.text
    await AllStates.next()
    await message.answer(text="Оно звенит? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.uh_q2)
async def u2_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_2'] = message.text
    await AllStates.next()
    await message.answer(text="Вы стали хуже слышать? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.uh_q3)
async def u3_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_3'] = message.text
    await AllStates.next()
    await message.answer(text="Вы болеете? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.uh_q4)
async def u4_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_4'] = message.text
    await AllStates.next()
    await message.answer(text="Сильно ли болит ухо? <b>\nДа/Нет</b>", parse_mode='HTML')


@dp.message_handler(state=AllStates.uh_q5)
async def u5_q(message: types.Message, state: AllStates):
    async with state.proxy() as data:
        data['1_5'] = message.text
    await AllStates.next()

    async with state.proxy() as data:
        # ответ на результаты исследования при выборе головы
        if (data['1_1'] == "Недавно" or data['1_1'] == "Не знаю") and data['1_2'] == "Нет" and data['1_3'] == "Да" \
                and data['1_4'] == "Да" and data['1_5'] == "Да":
            await message.answer(
                text="Возможно ухо болит из-за болезни, используйте капли для ушей и обратитесь к лору",
                reply_markup=kb.inline_kb1)

        elif (data['1_1'] == "Недавно" or data['1_1'] == "Не знаю") and data['1_2'] == "Нет" and data['1_3'] == "Да" \
                and data['1_4'] == "Нет" and data['1_5'] == "Нет":
            await message.answer(
                text="Возможно оно скоро пройдет, если нет, то обратитесь к врачу",
                reply_markup=kb.inline_kb1)

        elif (data['1_1'] == "Давно" or data['1_1'] == "Не знаю") and data['1_2'] == "Да" and data['1_3'] == "Да" \
                and data['1_4'] == "Да" and data['1_5'] == "Да":
            await message.answer(
                text="Обратись к лору, возможно что-то серьезное",
                reply_markup=kb.inline_kb1)

        elif (data['1_1'] == "Не знаю" or data['1_1'] == 'Недавно') and data['1_2'] == "Да" and data['1_3'] == "Да" \
                and data['1_4'] == "Нет" and data['1_5'] == "Нет":
            await message.answer(
                text="Попробуйте прочистить уши, возможно они забились")

        elif (data['1_1'] == "Нет" or data['1_1'] == "Не знаю") and data['1_2'] == "Нет" and data['1_3'] == "Нет" \
                and data['1_4'] == "Нет" and data['1_5'] == "Нет":
            await message.answer(text="Может у вас ничего не болит?", reply_markup=kb.inline_kb1)

        else:
            await message.answer(
                text="Советуем выпить лекарства и подождать,если не помогло - вернитесь назад и"
                     " нажмите на кнопку 📋 Записаться к врачу")

    await state.finish()


@dp.message_handler(text=['🏥 Выбрать больницу'])
async def hospital(message: types.Message):
    keyb = kb.make_keyboard("region", db.get_regions())
    await bot.send_message(chat_id=message.from_user.id,
                           text="Выберите регион",
                           reply_markup=keyb)


@dp.callback_query_handler(lambda message: message.data[:6] == "region")
async def region(callback_query: types.CallbackQuery):
    region_name = callback_query.data[6:]
    keyb = kb.make_keyboard("city", db.get_cities(region_name))
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Выберите город",
                           reply_markup=keyb)


@dp.callback_query_handler(lambda message: message.data[:4] == "city")
async def region(callback_query: types.CallbackQuery):
    city_name = callback_query.data[4:]
    db.set_city(city_name, callback_query.from_user.id)
    keyb = kb.make_keyboard("hospital", db.get_hospitals(city_name))
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Выберите больницу",
                           reply_markup=keyb)


@dp.callback_query_handler(lambda message: message.data[:8] == "hospital")
async def hospital(callback_query: types.CallbackQuery):
    hospital_name = callback_query.data[8:]
    info = db.get_info(db.get_city(callback_query.from_user.id), hospital_name)
    try:
        ll, spn = get_ll_span(info[2])

        if ll and spn:
            lon, lat = map(float, ll.split(','))
            point = "{ll},pm2vvl".format(ll=ll)
            static_api_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={point}".format(
                **locals())
            await bot.delete_message(chat_id=callback_query.from_user.id,
                                     message_id=callback_query.message.message_id)
            info_dc = kb.kb_docs(hospital_name)

            await bot.send_photo(chat_id=callback_query.from_user.id,
                                 photo=static_api_request,
                                 caption=f"{info[1]} {info[3]}",
                                 reply_markup=info_dc)
    except RuntimeError as ex:
        await bot.reply_text(str(ex))


@dp.message_handler(text=["☎ Обратиться в поддержку"])
async def waiting_for_support(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Администратор - @admin_id")


@dp.message_handler(text=["📷Загрузить фото"])
async def photo(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Отправьте свою фотографию",
                           reply_markup=kb.none)


@dp.message_handler(content_types=ContentType.PHOTO)
async def process_photo(message: types.Message):
    # Получаем список фотографий в сообщении
    photo = message.photo[-1]

    await bot.send_message(chat_id=message.from_user.id,
                           text="Фото загружено успешно!",
                           reply_markup=kb.lk_menu)
    # Обрабатываем фотографию (например, сохраняем ее в базу данных)
    db.set_photo(photo.file_id, message.from_user.id)


@dp.callback_query_handler(lambda message: message.data[:4] == "docs")
async def docs(callback_query: types.CallbackQuery):
    hospital = callback_query.data[4:]
    kb_dc = kb.make_dc_keyboard(hospital[:14], db.get_docs(hospital[:14]))
    print(kb_dc)
    id = callback_query.from_user.id
    await bot.send_message(chat_id=id,
                           text="Выберите специальность интересующего вас врача:",
                           reply_markup=kb_dc)


@dp.callback_query_handler(lambda message: message.data[:3] == "doc")
async def doc(callback_query: types.CallbackQuery):
    doc = callback_query.data[17:]
    hospital = callback_query.data[3:17]
    docs = db.get_doc(hospital, doc)
    print(docs)
    kb_who = kb.make_who(hospital, docs)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"Все {doc} в {hospital}",
                           reply_markup=kb_who)


@dp.callback_query_handler(lambda message: message.data[:3] == "who")
async def who(callback_query: types.CallbackQuery):
    hospital = callback_query.data[3:17]
    who = callback_query.data[17:]
    info = db.get_from_name(hospital, who)
    print(info)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"{who}\n"
                                f"Кабинет - {info[0][3]}\n"
                                f"Время приема - 9-14")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
