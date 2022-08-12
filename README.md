# Инструкции по развертыванию тестового приложения

1. Копировать репозиторий : git@github.com:Nikita-Kechaev/simple-tg-bot-parser.git
2. Создать ТГ бота. Инструкции: <https://core.telegram.org/bots>
3. В коревой директории создать файл .env (прим. env_example)
    * Указать API-Токен созданного бота
4. Создать виртуальное окружение:
    * python3 -m venv venv
5. Активировать виртуальное окружение:
    * source venv/bin/activate
6. Уcтановить зависимости:
    * pip install requirements.txt
7. Активировать бота:
    * python3 main.py
8. Декативировать бота:
    * Ctrl + C
