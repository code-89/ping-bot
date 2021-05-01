import os

from database import SUBSTATION_DB


def text_request(request):
    if len(request) > 1:
        try:
            ip_address = SUBSTATION_DB[request[0]]
            request_count = int(request[1])
            if 1 <= request_count <= 20:
                return ping(ip_address, request_count)
            else:
                return ping(ip_address)
        except Exception:
            return ping(SUBSTATION_DB[request[0]])
    return ping(SUBSTATION_DB[request[0]])


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
    if '<' in response:
        return ('Адрес ' + hostname + ' доступен! \u2705 \n'
                'Время ответа < 1 ms')
    elif 'TTL=' in response:
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
        try:
            time = response.split('=')[i]
        except IndexError:
            return '<Error: 1> ' + hostname + '\n<превышен интервал ожидания>'
        for char in time:
            if char.isdecimal():
                received_time += char
            else:
                continue
        time_response.append(received_time)
    return result(time_response, len(numbers_list), hostname)


def result(time_response, request_count, hostname):
    result = ''
    try:
        for i in range(request_count):
            result += 'Время ответа = ' + time_response[i] + ' ms \n'
    except IndexError:
        return '<Error: 2> ' + hostname + '\n<невозможно вывести результат>'
    return 'Адрес ' + hostname + ' доступен! \u2705 \n' + result
