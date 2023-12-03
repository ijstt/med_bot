from aiogram import types

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_btn1 = types.KeyboardButton("📋 Записаться к врачу")
main_btn2 = types.KeyboardButton("❤ Симптомы")
main_btn3 = types.KeyboardButton("🏠 Личный кабинет")
main_btn4 = types.KeyboardButton("🏥 Выбрать больницу")
main_btn5 = types.KeyboardButton("☎ Обратиться в техподдержку")
menu.add(main_btn3, main_btn2, main_btn1, main_btn4, main_btn5)

lk_menu = types.ReplyKeyboardMarkup(row_width=1)
doctor_btn = types.KeyboardButton("📋 Записаться к врачу")
back_btn = types.KeyboardButton("⬅ Назад")
lk_menu.add(doctor_btn, back_btn)

doctor = types.InlineKeyboardMarkup(row_width=1)
doctor_btn = types.InlineKeyboardButton("Перейти по ссылке", url="https://www.gosuslugi.ru/category/health",
                                        callback_data=None)
doctor.add(doctor_btn)

menu_simp = types.ReplyKeyboardMarkup(resize_keyboard=True)
simp_btn1 = types.KeyboardButton("🧠 Голова")
simp_btn2 = types.KeyboardButton("❤ Живот")
simp_btn3 = types.KeyboardButton("🦷 Зубы")
simp_btn4 = types.KeyboardButton("💪 Рука или нога")
simp_btn5 = types.KeyboardButton("👂 Ухо")
back_btn = types.KeyboardButton("⬅ Назад")
menu_simp.add(simp_btn1, simp_btn2, simp_btn3, simp_btn4, simp_btn5, back_btn)


def make_keyboard(key, data):
    tmp_keyboard = types.InlineKeyboardMarkup(row_width=1)
    for name in data:
        btn = types.InlineKeyboardButton(f"{name}", callback_data=f"{key}{name}")
        tmp_keyboard.add(btn)
    return tmp_keyboard
