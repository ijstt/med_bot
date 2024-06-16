from aiogram import types

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_btn1 = types.KeyboardButton("📋 Записаться к врачу")
main_btn2 = types.KeyboardButton("❤ Симптомы")
main_btn3 = types.KeyboardButton("🏠 Личный кабинет")
main_btn4 = types.KeyboardButton("🏥 Выбрать больницу")
main_btn5 = types.KeyboardButton("☎ Обратиться в поддержку")
menu.add(main_btn3, main_btn2, main_btn1, main_btn4, main_btn5)

admin_registr = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel = types.KeyboardButton("Отмена")
admin_registr.add(cancel)

admin_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel = types.KeyboardButton("Отмена")
admin_cancel.add(cancel)

doc_menu = types.InlineKeyboardMarkup()
doc_add = types.InlineKeyboardButton("Добавить врачей", callback_data="adddoc")
doc_del = types.InlineKeyboardButton("Удалить врача", callback_data="deldoc")
doc_menu.add(doc_del, doc_add)

admin_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
back = types.KeyboardButton("В главное меню")
hos = types.KeyboardButton("Добавить больницу")
doc = types.KeyboardButton("Редактировать врачей")
gor = types.KeyboardButton("Добавить город")
obl = types.KeyboardButton("Добавить область")
user = types.KeyboardButton("Удалить пользователя")
admin_menu.add(back, hos, doc, gor, obl, user)

lk_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
doctor_btn = types.KeyboardButton("📋 Записаться к врачу")
photo_btn = types.KeyboardButton("📷Загрузить фото")
admin_btn = types.KeyboardButton("Панель администратора")
back_btn = types.KeyboardButton("⬅ Назад")
lk_menu.add(doctor_btn, photo_btn, admin_btn, back_btn)

none = types.ReplyKeyboardRemove()

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


def kb_docs(hospital):
    info_dc = types.InlineKeyboardMarkup(row_width=1)
    info = types.InlineKeyboardButton("Врачи", callback_data=f"docs{hospital}")
    info_dc.add(info)
    return info_dc


test_dc = types.InlineKeyboardMarkup()
dc1 = types.InlineKeyboardButton("Невропатолог", callback_data="dc1")
dc2 = types.InlineKeyboardButton("Психиатр", callback_data="dc2")
dc3 = types.InlineKeyboardButton("Окулист", callback_data="dc3")
bck = types.InlineKeyboardButton("⬅", callback_data="bck")
num = types.InlineKeyboardButton("0/1", callback_data="0")
nxt = types.InlineKeyboardButton("➡", callback_data="nxt")
test_dc.add(dc1, dc2, dc3, bck, num, nxt)


def make_keyboard(key, data):
    tmp_keyboard = types.InlineKeyboardMarkup(row_width=1)
    for name in data:
        btn = types.InlineKeyboardButton(f"{name}", callback_data=f"{key}{name}")
        tmp_keyboard.add(btn)
    return tmp_keyboard


def make_who(hospital, data):
    tmp_who = types.InlineKeyboardMarkup()
    for name in data:
        btn = types.InlineKeyboardButton(f"{name[1]}", callback_data=f"who{hospital}{name[1]}")
        tmp_who.add(btn)
    bck = types.InlineKeyboardButton("⬅", callback_data=f"bckwho{hospital}")
    num = types.InlineKeyboardButton("1/1", callback_data=f"numwho{hospital}")
    nxt = types.InlineKeyboardButton("➡", callback_data=f"nxtwho{hospital}")
    tmp_who.add(bck, num, nxt)
    return tmp_who


def make_dc_keyboard(hospital, data):
    tmp_dc = types.InlineKeyboardMarkup()
    st = set()
    for row in data:
        if row[2] not in st:
            btn = types.InlineKeyboardButton(text=row[2], callback_data=f"doc{hospital}{row[2]}")
            tmp_dc.add(btn)
            st.add(row[2])
    bck = types.InlineKeyboardButton("⬅", callback_data=f"bck{hospital}")
    num = types.InlineKeyboardButton("1/1", callback_data=f"num{hospital}")
    nxt = types.InlineKeyboardButton("➡", callback_data=f"nxt{hospital}")
    tmp_dc.add(bck, num, nxt)
    return tmp_dc
