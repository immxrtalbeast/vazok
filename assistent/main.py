import eel
from fuzzywuzzy import fuzz
import config
import stt
import random
import requests
import json
import collections
import datetime

collections.Callable = collections.abc.Callable
Callable = collections.Callable

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNWFjMWY2M2Q4YjFiZjliNDhmZDI4ODYxYmE4OTRiYjVhMzg3M2M1OGZlNGU2NjMzMmU1ODgwZWJlZjNhZmM1ODY4NmVjMDYyODY4ZTBhNWUiLCJpYXQiOjE3MTY4ODQyMTYuODgzNjUyLCJuYmYiOjE3MTY4ODQyMTYuODgzNjU2LCJleHAiOjE3NDg0MjAyMTYuODc1NTYyLCJzdWIiOiIyMzkiLCJzY29wZXMiOltdfQ.yHfY7az_90Kezw1qSz3M1FsES63mBA024YCGfNRXoskv0bM4YnfTJ7irNdsvMKY7f_P11avqPdlNeERLoddOTHfuzNgrLS29vTIf8HlmESe4wEf-04fYkPADIlMVdJmuv45CIeny2HXfnIBQ78G1d1hBbSP8YXgVkHh3O-I8eTxb2Qgh43TIb2CYYW5ec3SDjKArDensLe98T3XR03YoHBx4g2TdJG5TYDnEyJsUzkWgk-mqhEbh0baBrNpKMrPKrJtiqKL0UdSjKD6RSETkUHqPu1mH4LHIf2AyDqGUKNnLEaWvL_cFXlOlbCDAkoqzCp6Vz0lkMKfZHv76NohBb61PNFU-clQo5Av3vSK-9CA2OaW9CYf62JwrBC4xxMk7UJxF1xlWxd9cjLu_DqhIRjUpDvee1EX2XbdlgSmEzDKGwbsNf7DpsJv9q1JlV4-6zboOAYUCtfw6AR0IskxTbV1LD-AYo_o8TEbQzNNfkDuNrvYs3TCdVD2rpDzKCsKJkMXUDmaUgtym-ZOEIqu_lZ15CrKN8jelwS7siDMVHYA406A_yyp7PJ6YF59rOMeXigX4gtcUhTrTfmvTaNMFzdosY1dKBc9wDD6ioVb5qVlsXD-7t_2Iv0YpcvrZCbf8CveY3obO1395JmUVFuTqREJnmQPtO_NxOKivxCb8N70'
headers2 = {"Authorization": f"Bearer {token}"}

url = "https://rostov.bulgakov.app/api/auth/signIn"
url_to_get = "https://rostov.bulgakov.app/api/v2/schedule/lessons?to=16.06.2024&from=10.06.2024&user_id=239"

eel.init('web')

Flag = False


@eel.expose
def getUserMessage(voice: str):
    cmd = recognize_cmd(filter_cmd(voice), 1)
    if cmd['cmd'] not in config.VA_CMD_DICT.keys():
        response = ("Что?")
    else:
        response = (execute_cmd(cmd['cmd']))
    return response


def filter_cmd(raw_voice: str):  # Убирает служебные слова
    cmd = raw_voice
    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str, quantity):  # Sravnivaet slova
    rc = {'cmd': '', 'percent': 0}
    if quantity == 1:
        for c, v in config.VA_CMD_DICT.items():

            for x in v:
                vrt = fuzz.token_sort_ratio(cmd, x)
                if vrt > rc['percent'] and vrt >= 60:
                    rc['cmd'] = c
                    rc['percent'] = vrt

        return rc
    else:
        cmd = cmd.lower()
        result = []
        key_words = []
        for x, y in config.VA_CMD_DICT.items():
            for i in y:
                if (i[:len(cmd)]) == cmd:
                    new_value = i.title().replace(' ', '_')
                    result.append(f"<li onclick=selectInput({[new_value]})>{i.title()}</li>")
                    key_words.append(y)
        return result, key_words


def execute_cmd(cmd: str):  # Ответ
    if cmd == 'help':
        return "Я умею: произносить время, рассказывать анекдоты"
    elif cmd == 'ctime':
        now = datetime.datetime.now()
        if len(str(now.minute)) == 1:
            minute = '0' + str(now.minute)
        else:
            minute = now.minute
        return f"Сейчас {now.hour}:{minute}"
    elif cmd == 'joke':
        return random.choice(config.VA_CMD_RESP['joke'])
    elif cmd in ('right now', 'schedule tomorrow', 'schedule all', 'schedule today'):
        return get_lessons(cmd)
    else:
        return config.VA_CMD_DICT[cmd]


def get_lessons(cmd):
    data = {"email": "ReintovSS22@rostov-don.ithub.ru", "password": "3P4XHpHc"}
    with requests.Session() as session:
        session.post(url, data=data).text.encode().decode('unicode-escape')
        session.get("https://rostov.bulgakov.app/schedule")
        data = session.get(url_to_get, headers=headers2).text
    data = json.loads(data)
    data = data['student']
    today = datetime.datetime.now().day
    now = datetime.datetime.now().time()
    config.VA_CMD_RESP[cmd] = ''
    for i in data:
        a = (i['date'][:10])
        date = datetime.datetime.strptime(a, "%Y-%m-%d")
        list = {0: "Понедельник",
                1: "Вторник",
                2: "Среда",
                3: "Четверг",
                4: "Пятница",
                5: "Суббота"}

        weekday = list[date.weekday()]

        if today == date.day:
            config.VA_CMD_RESP['schedule today'] += (
                f"{i['subjects'][0]['name']} {i['classroom']['name']} {i['time']}<br>")

        if today + 1 == date.day:
            config.VA_CMD_RESP['schedule tomorrow'] += (
                f"{i['subjects'][0]['name']} {i['classroom']['name']} {i['time']}<br>")

        config.VA_CMD_RESP['schedule all'] += (
            f"{weekday} - {i['subjects'][0]['name']} {i['classroom']['name']} {i['time']}<br>")
    if config.VA_CMD_RESP[cmd] == '':
        return 'Нет уроков.'
    else:
        return config.VA_CMD_RESP[cmd]


@eel.expose
def results_box(text):
    if len(text) >= 2:
        text_to_display, key_words = recognize_cmd(filter_cmd(text), 3)
        try:
            if len(text_to_display) <= 3:
                return text_to_display
        except:
            pass



@eel.expose
def start_or_stop_Record(x):
    global Flag
    if x == 1:
        Flag = True
    else:
        Flag = False





@eel.expose
def start_voice(x):
    global gen
    if x == 1:
        gen = stt.va_listen()
        return gen
    else:
        gen = '1'
        return gen


@eel.expose
def record_voice():
    return next(gen)


eel.start("index.html")
