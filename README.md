﻿# ping-bot
Telegram-бот для проверки доступности, подключённого к серверу, удалённого оборудования. Работает только в Windows.
Бот пингует отправленный ему адрес и возвращает время ответа. Количество отправленных запросов по умолчанию = 4.
Можно изменить количество запросов написав после адреса число от 1 до 20 включительно.
Так же бот может пинговать объекты по названию из базы database.py, при этом количество запросов всегда = 4.
В строке bot = telebot.TeleBot(TOKEN) заменить TOKEN на токен вашего бота, выданный @BotFather при создании,
пример: bot = telebot.TeleBot('jihg897nkldnyuij4oiym') # в данном случае это случайный набор символов, длина не соответствует длине настоящего токена.
Либо добавить переменную TOKEN, содержащую выданный @BotFather токен, в файл tokenfile.py в директории с файлом pingbot.py

