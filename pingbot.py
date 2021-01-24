import logging
import telebot
import time
from database import substation_db
from tokenfile import token
from windows import processing_request, ping

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'Start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Вас приветствует Пинг-бот.\n'
                                      'Функционал доступен по команде /help')


@bot.message_handler(commands=['help', 'Help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Доступные команды:\n'
                                      '/start - приветствие\n'
                                      '/help - помощь\n'
                                      '/p - пинг любого адреса\n'
                                      'Так же можно просто отправить '
                                      'номер подстанции, например: 405')


@bot.message_handler(commands=['p', 'P'])
def request_ping_small_p(message):
    request = message.text.split(' ')
    if len(request) <= 1:
        bot.send_message(message.chat.id, 'Некорректный запрос\n'
                                          'Пример: /p google.com\n'
                                          'После адреса можно указать '
                                          'количество отправляемых запросов, '
                                          'от 1 до 20 включительно. '
                                          'По умолчанию количество = 4')
    else:
        bot.send_message(message.chat.id, processing_request(request))


@bot.message_handler(content_types=['text'])
def send_text(message):
    if '/' in message.text:
        bot.send_message(message.chat.id, '<Неизвестная команда>\n'
                                          'Для вызова списка доступных команд '
                                          'отправьте /help')
    elif str(message.text) in substation_db:
        bot.send_message(message.chat.id,
                         ping(substation_db[str(message.text)]))
    else:
        bot.send_message(message.chat.id, 'Подстанция "' + str(message.text) +
                                          '" отсутствует в базе! \u274c')


logging.basicConfig(filename='error.log',
                    format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(e)
        time.sleep(15)