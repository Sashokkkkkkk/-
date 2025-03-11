Telegram Bot: Учет пропусков студентов
Описание
Этот код представляет собой Telegram-бота, который помогает старосте группы вести учет студентов, пропускающих пары. Бот предоставляет функционал для добавления прогульщиков, просмотра списка пропусков, очистки записей и других операций.

Основные функции
Запись прогульщиков
Бот позволяет выбирать студентов из списка и записывать их в файл с указанием даты и причины пропуска.

Данные сохраняются в файл прогульщики.txt.

Просмотр списка прогульщиков
Бот выводит список студентов, пропустивших пары за текущий месяц.

Очистка записей
Пользователь может удалить записи за конкретную дату.

Удобное меню
Бот использует интерактивные кнопки для взаимодействия с пользователем.

Структура кода
Язык программирования
Python.

Библиотека
pyTelegramBotAPI (для работы с Telegram Bot API).

Импорт библиотек
python
Copy
import telebot
import logging
from datetime import datetime
Настройка бота
python
Copy
BOT_API = 'ВАШ_ТОКЕН_БОТА'
bot = telebot.TeleBot(BOT_API)
logging.basicConfig(level=logging.INFO)
Глобальные переменные
python
Copy
storage = {}  # Словарь для временного хранения данных пользователя
Функции для работы с файлом
Запись данных в файл
python
Copy
def write_to_file(data):
    with open("прогульщики.txt", "a") as file:
        file.write(data + "\n")
Чтение данных из файла
python
Copy
def read_from_file():
    with open("прогульщики.txt", "r") as file:
        return file.readlines()
Фильтрация записей по месяцу
python
Copy
def filter_by_month(month):
    lines = read_from_file()
    return [line for line in lines if month in line]
Фильтрация записей по дате
python
Copy
def filter_by_day(date):
    lines = read_from_file()
    return [line for line in lines if date in line]
Обработчики команд
Команда /start
python
Copy
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Привет, староста! Я помогу тебе вести учет прогульщиков.")
    show_main_menu(message.chat.id)
Показ главного меню
python
Copy
def show_main_menu(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    btn1 = telebot.types.KeyboardButton('📋 Список студентов')
    btn2 = telebot.types.KeyboardButton('📜 Список прогульщиков')
    btn3 = telebot.types.KeyboardButton('🧹 Очистить список')
    markup.add(btn1, btn2, btn3)
    bot.send_message(chat_id, "Выбери действие:", reply_markup=markup)
Обработка выбора студентов
python
Copy
@bot.message_handler(func=lambda message: message.text == '📋 Список студентов')
def select_students(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    students = ["Белоусов Сергей", "Вершинин Никита", "Иванов Иван"]
    for student in students:
        markup.add(telebot.types.KeyboardButton(student))
    markup.add(telebot.types.KeyboardButton('✅ Готово'))
    bot.send_message(message.chat.id, "👥 Выбери студентов:", reply_markup=markup)
Обработка ввода данных
python
Copy
@bot.message_handler(func=lambda message: message.text == '✅ Готово')
def ask_for_date(message):
    bot.send_message(message.chat.id, "📅 Введите дату пропуска в формате ДД.ММ.ГГГГ:")
    bot.register_next_step_handler(message, ask_for_reason)
Обработка неизвестных команд
python
Copy
@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(message.chat.id, "❌ Неизвестная команда. Используйте кнопки.")
Пример взаимодействия
Пользователь запускает бота командой /start.

Бот выводит главное меню:

📋 Список студентов

📜 Список прогульщиков

🧹 Очистить список

Пользователь выбирает действие, например, добавляет прогульщиков:

Выбирает студентов из списка.

Указывает дату и причину пропуска.

Данные сохраняются в файл.

Преимущества бота
Удобство: Все действия выполняются через интерактивные кнопки.

Надежность: Проверка корректности ввода данных.

Гибкость: Возможность удалять записи за конкретную дату.



