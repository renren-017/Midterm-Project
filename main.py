import telebot
from telebot import TeleBot, types

import random
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('TOKEN')

text1 = """- Здравствуй! Неужто новичок? Я твой <b>{1.first_name}</b>. Но
 ты... Как там тебя.. {0.first_name}! Не обольщайся. Это моя работа,
 и всё тут! - Ты хоть знаешь, что такое текстовая ролевая?"""


@bot.message_handler(commands=['start'])
def welcome(message):
    st = open('\\Users\\Алтынай\\Desktop\\Mid\\hi.webp', 'rb')
    bot.send_sticker(message.chat.id, st)

    markup = types.InlineKeyboardMarkup(row_width=2)
    i = types.InlineKeyboardButton("Знаю", callback_data='good')
    i2 = types.InlineKeyboardButton("Совсем профан", callback_data='bad')

    markup.add(i, i2)
    bot.send_message(message.chat.id, text1.format(message.from_user,
                     bot.get_me()), parse_mode='html', reply_markup=markup)


text2 = """Что ж, тогда начнём с основ.
\n/Таким образом ты выделяешь действие персонажа
или описание происходящего вокруг/
\n"Вот так ты выделяешь мысль своего персонажа"
\n- А так ты завязываешь диалог с другим персонажем.
\n\nКомбинируя данные элементы, ты пишешь
посты в ролевой группе. \nДавай приведу пример:
\n- Соберись с духом, ну же! - /всё твердила себе Мари, нервно покусывая ногти
у двери главного волшебника. Его грозный лик на утреннем сборе нагнал
немало страху на юношеские сердца, поэтому отвлекать его от
важных дел молодой эльфийке казалось занятием весьма и весьма совестным./
\n"И что же делать, если он разгневается, и меня выдворят
с должности его помощника в первый же день работы?!"
"""


@bot.callback_query_handler(func=lambda call: True)
def KnowIt(call):
    if call.message:
        if call.data == 'good':
            bot.send_message(call.message.chat.id, "Прекрасно! Введите /info, "
                             "чтобы получить короткий гайд по работе бота")
        elif call.data == 'bad':
            bot.send_message(call.message.chat.id, text2)
            bot.send_message(call.message.chat.id, "Введите /info, чтобы "
                             "получить короткий гайд по работе бота")


text3 = """Основной функционал:
\n/get_top10rp - информация о десятке топ НРИ
\n/dice - бросок кубика D12
\n/r_city - вывод рандомного города:
\n/quick_access - клавиатура для упрощения
 работы с вышеупомянутыми функциями
\n\nВ планах на следующий апдейт:
\n/set_stats - утвердить статистику вашего персонажа в DnD
\n/get_stats - получить статистику вашего персонажа в DND"""


@bot.message_handler(commands=['info'])
def get_info(message):
    bot.send_message(message.chat.id, text3)


@bot.message_handler(commands=['r_city'])
def randcit(message):

    URL = 'https://randstuff.ru/city/'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 '
               'Safari/537.36', 'accept': '*/*'}

    def get_html(url, params=None):
        t = requests.get(url, headers=HEADERS, params=params)
        return t

    def get_city(html):
        soup = BeautifulSoup(html, 'html.parser')
        cname = soup.find('div', class_='city-name').get_text(strip=True)
        cin = soup.find('div', class_='city-country').get_text(strip=True)
        return (str(cname) + " - " + str(cin))

    def parse():
        html = get_html(URL)
        if html.status_code == 200:
            return get_city(html.text)
        else:
            print("Couldn't get the access")

    i = 0
    a = []
    while i < 20:
        l = parse()
        a.append(l)
        i = i + 1

    bot.send_message(message.chat.id, random.choice(a))


@bot.message_handler(commands=['get_top10rp'])
def top7(message):

    URL = 'https://geekster.ru/top10/top-7-nastolnyh-rolevyh-igr/'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
               'x64) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/86.0.4240.111 Safari/537.36',
               'accept': '*/*'}

    def get_html(url, params=None):
        t = requests.get(url, headers=HEADERS)
        return t

    def get_top3(html):
        soup = BeautifulSoup(html, 'html.parser')
        cname = soup.find_all('div', class_='wpb_column vc_column_container '
                              'vc_col-sm-12')

        info = []
        for i in cname[0]:
            """ info_content = i.find('div', class_='vc_column-inner') """
            info.append({
                'name': i.find('div', class_='wpb_wrapper').get_text
                (strip=True)
                })

        e = info
        return e

    html = get_html(URL)
    text4 = str(get_top3(html.text))

    with open('\\Users\\Алтынай\\Desktop\\Mid\\Pathfinder-Kingmaker-'
              'Siege-Art.jpg', 'rb') as f:
        bot.send_photo(message.chat.id, f, caption=text4)

    bot.send_message(message.chat.id, '<a href="https://geekster.ru/top10/'
                     'top-7-nastolnyh-rolevyh-igr/">Нажми, чтобы узнать '
                     'больше!</a>', parse_mode='html')


@bot.message_handler(commands=['dice'])
def dice(message):
    numb = random.randrange(1, 13)
    bot.reply_to(message, str(numb))


@bot.message_handler(commands=['quick_access'])
def quick_access(message):

    text = "Для пущего удобства :)"

    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    i = types.KeyboardButton("Бросить кубик 🎲")
    i2 = types.KeyboardButton("Рандомный город 🏙️")

    markup2.add(i, i2)
    bot.send_message(message.chat.id, text, reply_markup=markup2)


@bot.message_handler(content_types=['text'])
def dice_win(message):
    if message.chat.type == 'private':
        if message.text == "Бросить кубик 🎲":
            dice(message)
        elif message.text == "Рандомный город 🏙️":
            randcit(message)


bot.polling(none_stop=True, interval=0, timeout=20)
