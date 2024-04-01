VA_NAME = 'Вацок'

VA_VER = "0.1"

VA_ALIAS = ('зомби', 'зомбяш', 'зомбий', 'зомбяра', 'зомбик', 'зомбяр', 'зомбяшечка', 'зомб')

VA_TBR = ('скажи', 'покажи', 'ответь', 'произнеси', 'расскажи', 'сколько','как','есть ли','получить','помощь','где')

VA_CMD_DICT = {
    "help": ('список команд', 'команды', 'что ты умеешь', 'твои навыки', 'навыки', 'навыки', 'хелп', 'помощь'),
    "ctime": ('время', 'текущее время', 'сейчас времени', 'который час'),
    "joke": ('анекдот', 'рассмеши', 'шутка', ' шутку', 'пошути', 'развесели'),
    "schedule today": ('расписание на сегодня',  'что у меня сегодня', 'занятия на сегодня'),
    "right now": ('сейчас', 'прямо сейчас', 'какой урок сейчас'),
    "schedule tomorrow": ('расписание на завтра', 'что у меня завтра', 'занятия на завтра'),
    "schedule all": ('расписание на неделю', 'моё расписание', 'покажи расписание',  'занятия на неделю' ),
    "attestation": ('промежуточная аттестация', 'аттестация'),
    "assessment of work": ('система оценивание работ','ставят оценки','оценка'),
    "help with documentation" : ('документация',"с документацией","что делать с документами"),
    "cashback": ('кэшбек', 'кешбек', ' возврат кэшбека'),
    "paying for college":('оплата','помощь с оплатой','совершить оплату','оплатить'),
    "transition to higher education":('перевод на курс','перевод',' высшее образование','курс','какой курс'),
    "meals included in tuition fees":('питание','включает питание','оплата за питание','обучение с питанием'),
    "earnings while studying":('заработок','зарабатывать','возможен заработок','имеется заработок'),
    "work after college": ('трудоустройство во время обучения', 'работа после колледжа', 'найти работу после колледжа'),
    "support program for students with disabilities":('для студентов с ограниченными возможностями',''),
    "see the event poster":('посмотреть афишу','где афиша','найти афишу','мероприятия на афише'),
    "how to get to the congress hall":('дойти до конгресс холла','конгресс холл','вход в конгресс холл'),
    "how to reach the boiling point":('дойти до точки кипения','точка кипения','вход в точку кипения'),
    "how to get from the first building to the eighth":('где 8 корпус', 'дойти в 8 корпус','добраться в 8 корпус','попасть в 8 корпус'),
    "how i can find psychologist in college": ('найти психолога', 'находится психолог', 'нужен психолог', 'связаться с психологом', 'психолог'),
    "take part in events organized by the university?": ('мероприятия', 'будут мероприятия', 'найти мероприятие', 'начинается мероприятие','принимать участие в мероприятие','участвовать в мероприятиях'),
    "how to be volonteer": ('стать волонтером', 'получить информацию о волонтерах', 'быть волонтёром', "волонтерство"),
    "can students see a psychologist in college for free?":('посещение психолога бесплатно','прийти к психологу бесплатно','бесплатное занятие у психолога', 'психолог бесплатно'),
    "what documents are needed for admission?":('документы при поступлении','список документов','перечнь документов'),
    "Until what date can you submit documents?":('дата сдачи документов','крайний срок подачи документов','последний день сдачи документов'),
    "are there entrance exams":('вступительные экзамены','список вступительных экзаменов','экзамен','что за экзамены'),
    #"GANGA": ('crack'), WTF?
    "what faculties are there in college after 9th grade?":('факультеты после 9 класса','список факультетов после 9 класса','какие есть факультеты после 9 класса'),
    "what faculties are there in college after 10-11 grade":('факультеты после 10-11 класса','список факультетов после 10-11 класса','какие есть факультеты после 10-11 класса'),
    "what forms of training are possible full-time/correspondence/online?":('формы обучения','какие бывают формы обучения','возможно ли учиться зоачно','заочное обучение'),
    "how to find out about the results of admission":('результаты поступления','как узнать результаты поступления','узнать реезультат о поступлении'),
    "what opportunities are provided for nonresident students":('возможности для иногородних студентов','преимущества у иногородних студентоов','иногородний студент','для иногородного студента'),
    "Is it possible to receive a scholarship":('стипендия','как получить стипендию','возможность получить стипендию'),
    "Is there a possibility of training on a budget":('бюджетное обучение','как перейти на бюджетное обучение','обучение на бюджете','что сделать для бюджетного обчуения'),
    "what benefits are provided upon admission":('льготы при поступлении','льготы','дают льготы при поступлении'),




}


VA_CMD_RESP = {
    'help': "Я умею: произносить время, рассказывать анекдоты",
    'joke': ['Как смеются программисты? ... ехе ехе ехе',
                     'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «можно присоединиться?»',
                     'Программист это машина для преобразования кофе в код'],
    'schedule today': '',
    'right now': 'Сейчас нет уроков.',
    'schedule tomorrow': '',
    'schedule all': '',
    'attestation': '',
    'assessment of work': '',
    'help with documentation': '',
    'cashback': '',
    'paying for college': '',
    'transition to higher education': '',
    'meals included in tuition fees': '',
    'earnings while studying': '',
    'support program for students with disabilities': '',
    'see the event poster': '',
    'how to get to the congress hall': '',
    'how to reach the boiling point': '',
    'how to get from the first building to the eighth': '',
    'how i can find psychologist in collage': '',
    'take part in events organized by the university?': '',
    'how to be volonteer': '',
    'can students see a psychologist in college for free?': '',
    'what documents are needed for admission?': '',
    'Until what date can you submit documents?': '',
    'are there entrance exams': '',
    #'GANGA': '', motherfucker AKA SerjREY2007
    'what faculties are there in college after 9th grade?': '',
    'what faculties are there in college after 10-11 grade': '',
    'what forms of training are possible full-time/correspondence/online?': '',
    'how to find out about the results of admission': '',
    'what opportunities are provided for nonresident students': '',
    'Is it possible to receive a scholarship': '',
    'Is there a possibility of training on a budget': '',
    'what benefits are provided upon admission': '',
}


VA_CMD_LIST = ['список команд', 'команды', 'что ты умеешь', 'твои навыки',
               'навыки', 'навыки', 'хелп', 'помощь', 'время', 'текущее время',
               'сейчас времени', 'который час', 'расскажи анекдот', 'рассмеши',
               'шутка', 'расскажи шутку', 'пошути', 'развесели', 'расписание на сегодня',
               'что у меня сегодня', 'занятия на сегодня', 'сейчас', 'прямо сейчас', 'какой урок сейчас',
               'расписание на завтра', 'что у меня завтра', 'занятия на завтра', 'покажи расписание',
               'моё расписание', 'занятия на неделю', 'расписание на неделю']


