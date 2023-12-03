import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
import keyboard as kb
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
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Ваше имя - {db.get_name(message.from_user.id)}",
                           reply_markup=kb.lk_menu)


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
    region_name = callback_query.data[:6]
    keyb = kb.make_keyboard("city", db.get_cities(region_name))
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Выберите город",
                           reply_markup=keyb)


@dp.callback_query_handler(lambda message: message.data[:4] == "city")
async def region(callback_query: types.CallbackQuery):
    city_name = callback_query.data[:4]
    keyb = kb.make_keyboard("hospital", db.get_hospitals(city_name))
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Выберите больницу",
                           reply_markup=keyb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
