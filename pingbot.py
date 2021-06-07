import os
import telebot
import time

from dotenv import load_dotenv

from database import SUBSTATION_DB
from windows import processing_request, text_request

load_dotenv()
token = os.getenv('TOKEN')
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


def repeat(message):
    repeat_button = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True
    )
    return repeat_button.add(message.text)


@bot.message_handler(commands=['p', 'P'])
def request_command(message):
    request = message.text.split(' ')
    if len(request) <= 1:
        bot.send_message(message.chat.id, 'Некорректный запрос\n'
                                          'Пример: /p google.com\n'
                                          'После адреса можно указать '
                                          'количество отправляемых запросов, '
                                          'от 1 до 20 включительно. '
                                          'По умолчанию количество = 4')
    else:
        bot.send_message(message.chat.id, processing_request(request),
                         reply_markup=repeat(message))


@bot.message_handler(content_types=['text'])
def request_text(message):
    request = str(message.text).split(' ')
    if '/' in message.text:
        bot.send_message(message.chat.id, '<Неизвестная команда>\n'
                                          'Для вызова списка доступных команд '
                                          'отправьте /help')
    elif request[0] in SUBSTATION_DB:
        bot.send_message(message.chat.id, text_request(request),
                         reply_markup=repeat(message))
    else:
        bot.send_message(message.chat.id, 'Подстанция "' + str(message.text) +
                                          '" отсутствует в базе! \u274c',
                         reply_markup=repeat(message))


@bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker',
                                    'video', 'video_note', 'voice',
                                    'location', 'contact', 'new_chat_members',
                                    'left_chat_member', 'new_chat_title',
                                    'new_chat_photo', 'delete_chat_photo',
                                    'group_chat_created',
                                    'supergroup_chat_created',
                                    'channel_chat_created',
                                    'migrate_to_chat_id',
                                    'migrate_from_chat_id', 'pinned_message'])
def other_type(message):
    bot.send_message(message.chat.id, 'Бот понимает только команды и текст.\n'
                                      'Для помощи отправьте /help')


def logger(exception_type):
    with open('error.log', 'a') as logfile:
        error_time = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
        logfile.write(error_time + exception_type + '\n')


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger(str(type(e).__name__))
        time.sleep(15)
