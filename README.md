Бот для старосты @Hdjehevhehdh_bot
структура проекта
Copy
telegram-bot/

requirements.txt
Copy
pyTelegramBotAPI==4.12.0
bot.py
Импорт библиотек:

telebot, types, logging, datetime.

Настройка бота:

Инициализация бота с токеном.

Настройка логирования.

Глобальные переменные:

storage для временного хранения данных пользователя.

Функции для работы с файлом:

write_to_file: Запись данных о пропусках в файл.

read_from_file: Чтение данных из файла.

filter_by_month: Фильтрация записей по текущему месяцу.

filter_by_day: Фильтрация записей по конкретной дате.

Обработчики команд:

/start: Запуск бота и вывод главного меню.

Просмотр списка прогульщиков.

Очистка записей за конкретную дату.

Выбор студентов и запись их в список прогульщиков.

Обработка неизвестных команд:

Ответ на неизвестные команды.

Запуск бота:

bot.polling() для запуска бота.

README.md
markdown
Copy
 Telegram Bot: Учет пропусков студентов

Этот Telegram-бот помогает старосте группы вести учет студентов, пропускающих пары.

 Основные функции

- **Запись прогульщиков**: Выбор студентов и запись их в файл с указанием даты и причины пропуска.
- **Просмотр списка прогульщиков**: Вывод списка студентов, пропустивших пары за текущий месяц.
- **Очистка записей**: Удаление записей за конкретную дату.
- **Удобное меню**: Интерактивные кнопки для взаимодействия.

 Установка и запуск

1. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

2. Создайте файл `.env` и добавьте токен бота:

    ```env
    BOT_API=ВАШ_ТОКЕН_БОТА
    ```

3. Запустите бота:

    ```bash
    python bot.py
    ```

 Используемые технологии

- Python 3.9+
- pyTelegramBotAPI
- Logging
- Datetime

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
