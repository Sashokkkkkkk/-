import telebot
from telebot import types
import logging
from datetime import datetime

BOT_API = '7780827860:AAGay5RraBPn8kvoCoRUM4yXolfI7RDVhho'

bot = telebot.TeleBot(BOT_API)
telebot.logger.setLevel(logging.INFO)

storage = dict()

def write_to_file(student_names, date, pair_info):
    with open("прогульщики.txt", "a", encoding="utf-8") as file:
        for student_name in student_names:
            file.write(f"{student_name} - {date} - {pair_info}\n")

def read_from_file():
    try:
        with open("прогульщики.txt", "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def filter_by_month(entries):
    current_month = datetime.now().strftime("%m.%Y")
    return [entry for entry in entries if current_month in entry]

def filter_by_day(entries, date):
    return [entry for entry in entries if date in entry]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('/students')
    btn2 = types.KeyboardButton('/list')
    btn3 = types.KeyboardButton('/clear')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, '''
Привет староста, выбери что ты хочешь знать:
Чтобы вывести список студентов, нажми на кнопку /students
Чтобы вывести список прогульщиков, используйте команду /list
Чтобы очистить список прогульщиков, используйте команду /clear

                     ''', reply_markup=markup)

@bot.message_handler(commands=['list'])
def send_list(message):
    entries = read_from_file()
    monthly_entries = filter_by_month(entries)
    if monthly_entries:
        bot.send_message(message.chat.id, f"Список прогульщиков за текущий месяц:\n{''.join(monthly_entries)}")
    else:
        bot.send_message(message.chat.id, "Список прогульщиков за текущий месяц пуст.")

@bot.message_handler(commands=['clear'])
def clear_list(message):
    bot.send_message(message.chat.id, "Введите дату для очистки в формате ДД.ММ.ГГГГ:")
    bot.register_next_step_handler(message, handle_clear_date)

def handle_clear_date(message):
    date = message.text
    try:
        datetime.strptime(date, "%d.%m.%Y")  # Проверка корректности даты
        entries = read_from_file()
        remaining_entries = [entry for entry in entries if date not in entry]
        with open("прогульщики.txt", "w", encoding="utf-8") as file:
            file.writelines(remaining_entries)
        bot.send_message(message.chat.id, f"Записи за {date} удалены.")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный формат даты. Используйте формат ДД.ММ.ГГГГ.")

@bot.message_handler(func=lambda message: message.text == '/students')
def handle_students(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('Белоусов Сергей', callback_data='Белоусов Сергей')
    btn3 = types.InlineKeyboardButton('Вершинин Никита', callback_data='Вершинин Никита')
    btn4 = types.InlineKeyboardButton('Горшенина Олеся', callback_data='Горшенина Олеся')
    btn5 = types.InlineKeyboardButton('Девятов Николай', callback_data='Девятов Николай')
    btn6 = types.InlineKeyboardButton('Домнин Дмитрий', callback_data='Домнин Дмитрий')
    btn7 = types.InlineKeyboardButton('Жигалов Данил', callback_data='Жигалов Данил')
    btn8 = types.InlineKeyboardButton('Загребина Софья', callback_data='Загребина Софья')
    btn9 = types.InlineKeyboardButton('Зайков Александр', callback_data='Зайков Александр')
    btn10 = types.InlineKeyboardButton('Зорина Александра', callback_data='Зорина Александра')
    btn11 = types.InlineKeyboardButton('Кельмаков Сергей', callback_data='Кельмаков Сергей')
    btn12 = types.InlineKeyboardButton('Корепанов Иван', callback_data='Корепанов Иван')
    btn13 = types.InlineKeyboardButton('Кочанов Александр', callback_data='Кочанов Александр')
    btn14 = types.InlineKeyboardButton('Кузьмин Иван', callback_data='Кузьмин Иван')
    btn15 = types.InlineKeyboardButton('Наговицын Ян', callback_data='Наговицын Ян')
    btn16 = types.InlineKeyboardButton('Петров Роман', callback_data='Петров Роман')
    btn17 = types.InlineKeyboardButton('Пронин Данил', callback_data='Пронин Данил')
    btn18 = types.InlineKeyboardButton('Соловьева Татьяна', callback_data='Соловьева Татьяна')
    btn19 = types.InlineKeyboardButton('Соловьев Константин', callback_data='Соловьев Константин')
    btn20 = types.InlineKeyboardButton('Тихонов Егор', callback_data='Тихонов Егор')
    btn21 = types.InlineKeyboardButton('Тронин Илья', callback_data='Тронин Илья')
    btn22 = types.InlineKeyboardButton('Чутов Кирилл', callback_data='Чутов Кирилл')
    btn23 = types.InlineKeyboardButton('Шувалов Андрей', callback_data='Шувалов Андрей')
    btn24 = types.InlineKeyboardButton('Готово', callback_data='Готово')
    markup.add(btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn15, btn16, btn17, btn18, btn19, btn20, btn21, btn22, btn23, btn24)
    bot.send_message(message.chat.id, 'Выбери студентов:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    user_id = call.from_user.id
    if user_id not in storage:
        storage[user_id] = {'students': []}
    
    student_name = call.data
    if student_name == 'Готово':
        if storage[user_id]['students']:
            bot.send_message(call.message.chat.id, "Введите дату пропуска в формате ДД.ММ.ГГГГ:")
            bot.register_next_step_handler(call.message, handle_date)
        else:
            bot.send_message(call.message.chat.id, "Вы не выбрали ни одного студента.")
    else:
        if student_name in storage[user_id]['students']:
            storage[user_id]['students'].remove(student_name)
        else:
            storage[user_id]['students'].append(student_name)

def handle_date(message):
    user_id = message.from_user.id
    student_data = storage.get(user_id)
    if student_data:
        student_data['date'] = message.text
        bot.send_message(message.chat.id, "Введите номер пары или описание пропущенной пары:")
        bot.register_next_step_handler(message, handle_pair_info)

def handle_pair_info(message):
    user_id = message.from_user.id
    student_data = storage.get(user_id)
    if student_data:
        student_names = student_data['students']
        date = student_data['date']
        pair_info = message.text
        write_to_file(student_names, date, pair_info)
        del storage[user_id]
        bot.send_message(message.chat.id, f"Студенты {', '.join(student_names)} записаны в список прогульщиков с датой {date} и пропущенной парой: {pair_info}.")

bot.polling()
