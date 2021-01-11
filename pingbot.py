import os
import telebot
from tokenfile import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Вас приветствует Пинг-бот.\n'
                                      'Функционал доступен по команде /help')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Доступные команды:\n'
                                      '/start - приветствие\n'
                                      '/help - помощь\n'
                                      '/P или /p - пинг')


@bot.message_handler(commands=['P'])
def request_ping_big_p(message):
    request = message.text.split(' ')
    if len(request) <= 1:
        bot.send_message(message.chat.id, 'Некорректный запрос\n'
                                          'Пример запроса: /P google.com\n'
                                          'После адреса можно указать '
                                          'количество отправляемых запросов, '
                                          'от 1 до 20 включительно. '
                                          'По умолчанию количество '
                                          'запросов = 4')
    else:
        bot.send_message(message.chat.id, processing_request(request))


@bot.message_handler(commands=['p'])
def request_ping_small_p(message):
    request = message.text.split(' ')
    if len(request) <= 1:
        bot.send_message(message.chat.id, 'Некорректный запрос\n'
                                          'Пример запроса: /P google.com\n'
                                          'После адреса можно указать '
                                          'количество отправляемых запросов, '
                                          'от 1 до 20 включительно. '
                                          'По умолчанию количество '
                                          'запросов = 4')
    else:
        bot.send_message(message.chat.id, processing_request(request))


@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, 'Бот понимает только команды.\n'
                                      'Для помощи введите /help')


def processing_request(request):
    if len(request) >= 3:
        try:
            request_count = int(request[2])
            if 1 <= request_count <= 20:
                return ping(request[1], request_count)
            else:
                return ping(request[1])
        except ValueError:
            return ping(request[1])
    else:
        return ping(request[1])


def ping(hostname, request_count=4):
    response = os.popen('ping ' + hostname + ' -n ' +
                        str(request_count)).read()
    if 'TTL=' in response:
        return response_parse(response, numbers_for_parse(request_count),
                                hostname)
    else:
        return 'Адрес ' + hostname + ' не доступен :( \u26d4\ufe0f'


def numbers_for_parse(request_count):
    numbers_list = [2]
    for i in range(request_count - 1):
        numbers_list.append(numbers_list[i] + 3)
    return numbers_list


def response_parse(response, numbers_list, hostname):
    time_response = []
    for i in numbers_list:
        received_time = ''
        time = response.split('=')[i]
        for char in time:
            try:
                num = int(char)
                received_time += char
            except ValueError:
                continue
        time_response.append(int(received_time))
    return result(time_response, len(numbers_list), hostname)


def result(time_response, request_count, hostname):
    result = ''
    for i in range(request_count):
        result += 'Время ответа = ' + str(time_response[i]) + ' ms \n'
    return 'Адрес ' + hostname + ' доступен! \u2705 \n' + result


bot.polling(none_stop=True)
