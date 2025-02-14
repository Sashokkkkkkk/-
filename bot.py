import telebot
from telebot import types
import logging
from datetime import datetime

BOT_API = 'YOU_BOT_API'

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
    btn1 = types.KeyboardButton('📋 Список студентов')
    btn2 = types.KeyboardButton('📜 Список прогульщиков')
    btn3 = types.KeyboardButton('🧹 Очистить список')
    markup.add(btn1, btn2, btn3)
    bot.send_message(
        message.chat.id,
        "👋 Привет, староста! Я помогу тебе вести учет прогульщиков.\n\n"
        "Выбери действие:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == '📜 Список прогульщиков')
def send_list(message):
    entries = read_from_file()
    monthly_entries = filter_by_month(entries)
    if monthly_entries:
        bot.send_message(message.chat.id, f"📅 Список прогульщиков за текущий месяц:\n\n{''.join(monthly_entries)}")
    else:
        bot.send_message(message.chat.id, "✅ Список прогульщиков за текущий месяц пуст.")

@bot.message_handler(func=lambda message: message.text == '🧹 Очистить список')
def clear_list(message):
    bot.send_message(message.chat.id, "📅 Введите дату для очистки в формате ДД.ММ.ГГГГ:")
    bot.register_next_step_handler(message, handle_clear_date)

def handle_clear_date(message):
    date = message.text
    try:
        datetime.strptime(date, "%d.%m.%Y")   
        entries = read_from_file()
        remaining_entries = [entry for entry in entries if date not in entry]
        with open("прогульщики.txt", "w", encoding="utf-8") as file:
            file.writelines(remaining_entries)
        bot.send_message(message.chat.id, f"✅ Записи за {date} успешно удалены.")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Некорректный формат даты. Используйте формат ДД.ММ.ГГГГ.")

@bot.message_handler(func=lambda message: message.text == '📋 Список студентов')
def handle_students(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    students = [
        'Белоусов Сергей', 'Вершинин Никита', 'Горшенина Олеся', 'Девятов Николай',
        'Домнин Дмитрий', 'Жигалов Данил', 'Загребина Софья', 'Зайков Александр',
        'Зорина Александра', 'Кельмаков Сергей', 'Корепанов Иван', 'Кочанов Александр',
        'Кузьмин Иван', 'Наговицын Ян', 'Петров Роман', 'Пронин Данил',
        'Соловьева Татьяна', 'Соловьев Константин', 'Тихонов Егор', 'Тронин Илья',
        'Чутов Кирилл', 'Шувалов Андрей'
    ]
    buttons = [types.InlineKeyboardButton(student, callback_data=student) for student in students]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton('✅ Готово', callback_data='Готово'))
    bot.send_message(message.chat.id, "👥 Выбери студентов:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    user_id = call.from_user.id
    if user_id not in storage:
        storage[user_id] = {'students': []}
    
    student_name = call.data
    if student_name == 'Готово':
        if storage[user_id]['students']:
            bot.send_message(call.message.chat.id, f"📝 Вы выбрали:\n{', '.join(storage[user_id]['students'])}\n\n📅 Введите дату пропуска в формате ДД.ММ.ГГГГ:")
            bot.register_next_step_handler(call.message, handle_date)
        else:
            bot.send_message(call.message.chat.id, "❌ Вы не выбрали ни одного студента.")
    else:
        storage[user_id]['students'].append(student_name)   
        bot.answer_callback_query(call.id, f"✅ {student_name} добавлен в список.")

def handle_date(message):
    user_id = message.from_user.id
    student_data = storage.get(user_id)
    if student_data:
        date = message.text
        try:
            datetime.strptime(date, "%d.%m.%Y")  
            student_data['date'] = date
            bot.send_message(message.chat.id, "📚 Введите номер пары или описание пропущенной пары:")
            bot.register_next_step_handler(message, handle_pair_info)
        except ValueError:
            bot.send_message(message.chat.id, "❌ Некорректный формат даты. Используйте формат ДД.ММ.ГГГГ.")
            bot.register_next_step_handler(message, handle_date)   

def handle_pair_info(message):
    user_id = message.from_user.id
    student_data = storage.get(user_id)
    if student_data:
        student_names = student_data['students']
        date = student_data['date']
        pair_info = message.text
        if pair_info.strip():   
            write_to_file(student_names, date, pair_info)
            del storage[user_id]  
            bot.send_message(
                message.chat.id,
                f"✅ Студенты {', '.join(student_names)} записаны в список прогульщиков.\n"
                f"📅 Дата: {date}\n"
                f"📚 Пропущенная пара: {pair_info}"
            )
        else:
            bot.send_message(message.chat.id, "❌ Информация о паре не может быть пустой. Попробуйте снова.")
            bot.register_next_step_handler(message, handle_pair_info)  

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(message.chat.id, "❌ Неизвестная команда. Используйте кнопки для взаимодействия.")

bot.polling()
