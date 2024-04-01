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

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZTBkNjBmMTI1MmQyZTFkMWY3NGY1YWYyNWFmNDRiMTJiMjZjYzAxNTgxMjExZTdmMWZjMDJmNTMyNzVjODY4ZGVkMmVmYWFiNTA3YjNhMzMiLCJpYXQiOjE3MTExMzU0MzcuMzYzODUyLCJuYmYiOjE3MTExMzU0MzcuMzYzODU0LCJleHAiOjE3NDI2NzE0MzcuMzU3OTM4LCJzdWIiOiIyMzkiLCJzY29wZXMiOltdfQ.YHXxWTVHNWNf_Vv9u3Sjo7P_wGh47BvNKikKIRpKAgwAAsq-E2RpE23F4pGawfpYGN5aUKOlMCOhISkaZMlfqucvC_dsGX4FfUdY6M4etoZjdcPux7ZZNDqSR_OWXc_hQcO-JwSx8RpyQJ6TjfJqIayoL_52pPoCcKpkEnIyGdnsCemOoJhnV5iNGhxhOjemPv89Za-slWrLKjgd3i7XrFVR3F6SKWx66L9FZiHYjp5xVMX24Z5f7I-5KQxLX3gbG_lImjxGAfShxNUfn1agSJly2fbAWSq7iNQq_v7P9rUCgWyvkkvTDJVp3jRc8qEnudDTqGuCb02veXf0TUhxGpwkG8Dqtv_ZTaoT-6q03lIqfI8aM4Wt8TOfeu0b8zE-fA6ZW_GOFxlIMd7A5unyQCOrEl9YFOeA5sK1mGR6SLGenulY9ydzG5aLSW-q1VfW4kMC9opo02rA5uK6KGyfqt_M6MKkAjExvrFOQzsiMp0CVPgIM7s122xYzmhGzADIkzQAYRqTGfy9fWiHo0ejKqJLArpotfGLaT7N5Zm3uCBedhjStc7XqTg-WHdhGeOcZf7yJwZHx1vI-YtB-ohaCLx-Wk7g9VcY05U3Ai32jAoqxerKgaQmYAxZwffyqCBpxw745laRC2d3n85FN78o2oo5BFFyRBFQ1xjQ5R8Mdog"
headers2 = {"Authorization": f"Bearer {token}"}

url = "https://rostov.bulgakov.app/api/auth/signIn"
url_to_get = "https://rostov.bulgakov.app/api/v2/schedule/lessons?to=31.03.2024&from=25.03.2024&user_id=239"

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
