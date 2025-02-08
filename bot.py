import telebot
from telebot import types
import logging

BOT_API = '7780827860:AAGay5RraBPn8kvoCoRUM4yXolfI7RDVhho'  # Замените на ваш токен

bot = telebot.TeleBot(BOT_API)
telebot.logger.setLevel(logging.INFO)

storage = dict()

# Функция для записи фамилии студента в файл
def write_to_file(student_name):
    with open("прогульщики.txt", "a", encoding="utf-8") as file:
        file.write(student_name + "\n")

# Функция для чтения содержимого файла
def read_from_file():
    try:
        with open("прогульщики.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Список прогульщиков пуст."

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Студенты', callback_data='Stydentu')
    markup.add(btn1)
    bot.send_message(message.chat.id, '''
Чтобы вывести список прогульщиков, используйте команду /list
Чтобы очистить список прогульщиков, используйте команду /clear
Привет староста, выбери что ты хочешь знать:
                     ''', reply_markup=markup)

# Команда /list для вывода списка прогульщиков
@bot.message_handler(commands=['list'])
def send_list(message):
    list_content = read_from_file()
    bot.send_message(message.chat.id, f"Список прогульщиков:\n{list_content}")

@bot.message_handler(commands=['clear'])
def clear_list(message):
    open("прогульщики.txt", "w", encoding="utf-8").close()
    bot.send_message(message.chat.id, "Список прогульщиков очищен.")

# Обработчик callback_data
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'Stydentu':
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
        markup.add(btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn15, btn16, btn17, btn18, btn19, btn20, btn21, btn22, btn23)
        bot.send_message(call.message.chat.id, 'Выбери студента:', reply_markup=markup)
    
    else:
        # Если callback_data не 'Stydentu', значит это фамилия студента
        student_name = call.data
        write_to_file(student_name)  # Записываем фамилию студента в файл
        bot.answer_callback_query(call.id, f"{student_name} записан в список прогульщиков.")



# Запуск бота
bot.polling()