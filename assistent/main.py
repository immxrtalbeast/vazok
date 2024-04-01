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

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMWE1YTMxMDdiNWQ3NzFmYTc5ZjdkZjEyNzcwMTczYjQ2MjJhZDg5MTk4N2FlZmU4M2Q3OGFiM2VjMjkwMWU4OTgzYWVjOTFhYWU4NmYzOTAiLCJpYXQiOjE3MTE5ODYzMDguNzAxMTQzLCJuYmYiOjE3MTE5ODYzMDguNzAxMTQ4LCJleHAiOjE3NDM1MjIzMDguNjkwODg2LCJzdWIiOiIyMzkiLCJzY29wZXMiOltdfQ.qJHR3iYXd9tLAoEGMOnADmJoFQBrInW7BZh67aHePlIP_LkOqG_I8_Mvx0_9Z_N-D9qInK7acucT5TX3uIXWjrZk4hvTpz39hUPu9C4al4GvJQgb_F338TC74cYu9gHJVJj2IigCUgkIP3P8VKx39COFoI9vJhfSyKw4LF3EKPFu3-tsLO1OuSgwHQjp6O26E_xJdPF8WaaD3jFVjWMx17lCD8Gkt2na8QDgbQQJ5HdLAO_VsQtNSabpHub8nm8LEs8-P5bU-ZRZfkxheSXgNOCeJXuMRZzkiXdOs9Y4e08t4NzNPi41XzwlCIYEebVeWvhkW_gnKQd9pO_DPSCym2DNNIejjwhBMo4phyqh7nN5z4zxOyP72W_e9DBwGnkIh9Z71cn-MRW8_ZJXftqeXyWvmOW2iOMRmCaVKK5O2AhR8q7OsHr3GRp085_wRryafjjaM5XTIcbUO2VnX88TvkUMzhzeaAV85BVx8ZO5OZEygvHFBCYAZpWJcRhjk6XT8jeeM3PPu84Wm5uY1c9HdHxOg8YMulpV-Qla9khFkugFlShSnIwLbY6gfwhHQWf5j1zCIAu_8piTLnH1hnabrAb2c6aWd9nEjyb6emZoJo2kfVUxUtVVSWHcXyE4HuIF2r_wReLYwgRcxA6uDlqHOk_-t3OQ3AroFh_Dm7IM-YM"
headers2 = {"Authorization": f"Bearer {token}"}

url = "https://rostov.bulgakov.app/api/auth/signIn"
url_to_get = "https://rostov.bulgakov.app/api/v2/schedule/lessons?to=07.04.2024&from=01.04.2024&user_id=239"

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
