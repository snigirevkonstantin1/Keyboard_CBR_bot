#trykeyboard_bot
import telebot
from telebot import types
import time
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import os
from flask import Flask, request
from telebot import apihelper


server = Flask(__name__)


token = 'YOUR_SECRET_TOKEN'
bot = telebot.TeleBot(token)
user_state = defaultdict(lambda: valute)
products = defaultdict(lambda: {})
currensi = ['RU', 'AUD', 'AZN', 'GBP', 'AMD', 'BYN', 'BGN', 'BRL',
            'HUF', 'HKD', 'DKK', 'USD', 'EUR', 'INR', 'KZT',
            'CAD', 'KGS', 'CNY', 'MDL', 'NOK', 'PLN', 'RON',
            'XDR', 'SGD', 'TJS', 'TRY', 'TMT', 'UZS', 'UAH',
            'CZK', 'SEK', 'CHF', 'ZAR', 'KRW', 'JPY']
valute_dict = {'RU':'Российский рубль', 'AUD': 'Австралийский доллар', 'AZN': 'Азербайджанский манат',
                'GBP': 'Фунт стерлингов Соединенного королевства', 'AMD': 'Армянских драмов',
                'BYN': 'Белорусский рубль', 'BGN': 'Болгарский лев', 'BRL': 'Бразильский реал',
                'HUF': 'Венгерских форинтов', 'HKD': 'Гонконгских долларов', 'DKK': 'Датских крон',
                'USD': 'Доллар США', 'EUR': 'Евро', 'INR': 'Индийских рупий', 'KZT': 'Казахстанских тенге',
                'CAD': 'Канадский доллар', 'KGS': 'Киргизских сомов', 'CNY': 'Китайских юаней', 'MDL': 'Молдавских леев',
                'NOK': 'Норвежских крон', 'PLN': 'Польский злотый', 'RON': 'Румынский лей',
                'XDR': 'СДР (специальные права заимствования)', 'SGD': 'Сингапурский доллар',
                'TJS': 'Таджикских сомони', 'TRY': 'Турецкая лира', 'TMT': 'Новый туркменский манат',
                'UZS': 'Узбекских сумов', 'UAH': 'Украинских гривен', 'CZK': 'Чешских крон',
                'SEK': 'Шведских крон', 'CHF': 'Швейцарский франк', 'ZAR': 'Южноафриканских рэндов',
                'KRW': 'Вон Республики Корея', 'JPY': 'Японских иен'}
valute_dicts = str(valute_dict)


def prettyprint(count, string):
    naminal_dict = {'AUD': ['Австралийский доллар', 'Австралийских доллара', 'Австралийских долларов'],
                    'AZN': ['Азербайджанский манат', 'Азербайджанских маната', 'Азербайджанских манатов'],
                    'GBP': ['Фунт стерлингов Соединенного королевства', 'Фунта стерлингов Соединенного королевства',
                            'Фунтов стерлингов Соединенного королевства'],
                    'AMD': ['Армянский драм', 'Армянских драма', 'Армянских драмов'],
                    'BYN': ['Белорусский рубль', 'Белорусских рубля', 'Белорусских рублей'],
                    'BGN': ['Болгарский лев', 'болгарского лева', 'болгарских левов'],
                    'BRL': ['Бразильский реал', 'бразильского реала', 'бразильских реалов'],
                    'HUF': ['Венгерский форинт', 'Венгерских форинта', 'Венгерских форинтов'],
                    'HKD': ['Гонконгский доллар', 'Гонконгских доллара', 'Гонконгских долларов'],
                    'DKK': ['Датская крона', 'датской кроны', 'датских крон'],
                    'USD': ['Доллар США', 'Доллара США', 'Долларов США'],
                    'EUR': ['Евро', 'Евро', 'Евро'],
                    'INR': ['Индийская рупия', 'Индийских рупий', 'Индийских рупий'],
                    'KZT': ['Казахстанский тенге', 'Казахстанских тенге', 'Казахстанских тенге'],
                    'CAD': ['Канадский доллар', 'Канадских доллара', 'Канадских долларов'],
                    'KGS': ['Киргизский сом', 'Киргизского сома', 'Киргизских сомов'],
                    'CNY': ['Китайских юань', 'Китайских юаня', 'Китайских юаней'],
                    'MDL': ['Молдавский леев', 'Молдавских лея', 'Молдавских леев'],
                    'NOK': ['Норвежских крон', 'Норвежских крон', 'Норвежских крон'],
                    'PLN': ['Польский злотый', 'Польских злотых', 'Польских злотых'],
                    'RON': ['Румынский лей', 'Румынских лей', 'Румынских лей'],
                    'XDR': ['СДР (специальные права заимствования)', 'СДР (специальных права заимствования)',
                            'СДР (специальных права заимствования)'],
                    'SGD': ['Сингапурский доллар', 'Сингапурских доллара', 'Сингапурских долларов'],
                    'TJS': ['Таджикских сомони', 'Таджикских сомони', 'Таджикских сомони'],
                    'TRY': ['Турецкая лира', 'турецких лир', 'турецких лир'],
                    'TMT': ['Новый туркменский манат', 'Новых туркменских манат', 'Новых туркменскийх манатов'],
                    'UZS': ['Узбекский сум', 'Узбекских сумов', 'Узбекских сумов'],
                    'UAH': ['Украинских гривен', 'украинских гривен', 'украинских гривен'],
                    'CZK': ['Чешская крона', 'Чешских кроны' 'Чешских крон'],
                    'SEK': ['Шведская крона', 'Шведских кроны', 'Шведских крон'],
                    'CHF': ['Швейцарский франк', 'Швейцарским франкам', 'Швейцарским франкам'],
                    'ZAR': ['Южноафриканский рэнд', 'Южноафриканских рэнда', 'Южноафриканских рэндов'],
                    'KRW': ['Вон Республики Корея', 'Вона Республики Кореи', 'Вонов Республикии Кореи'],
                    'JPY': ['Японский иен', 'Японских иены', 'Японских иен'],
                    'RU': ['Рубль', 'Рубля', 'Рублей']}
    if int(count) % 10 == 1:
        if count[:2] == '11':
            naminal_dict.get(string)[2]
        else:
            return naminal_dict.get(string)[0]
    if (1 < (int(count) % 10) < 5):
        if count[:2] == '12' or count[:2] == '13' or count[:2] == '14':
            return naminal_dict.get(string)[2]
        else:
            return naminal_dict.get(string)[1]
    else:
        return naminal_dict.get(string)[2]


valute, tovalute, nominal, getter, see = range(5)
def keyboard():
    key = types.InlineKeyboardMarkup(row_width=4)
    buttons = [types.InlineKeyboardButton (text=valute, callback_data=valute) for valute in currensi]
    key.add(*buttons)
    return key


def again_button():
    againbutton = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton('/convert')
    againbutton.add(button)
    return againbutton


def onekey():
    onekbutton = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton('Далее')
    onekbutton.add(button)
    return onekbutton


def noonekey():
    onekbutton = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton('Да')
    button2 = types.KeyboardButton('Нет')
    onekbutton.add(button1, button2)
    return onekbutton


@bot.message_handler(commands=['start'])
def handle_start(message):
    key = keyboard()
    bot.send_message(message.chat.id, text='Здравствуйте. \n Данный бот выполняет функции калькулятора валют. Данные берутся c сайта центра банка РФ на сегодняшнею дату.В зависимости от количества валюты бот пытается склонять ответное сообщение.\nРабота с ботом: для калькулятора валют напишите команду /convert ' \
      '\n1. Указываете в какую валюту переводить.' \
      '\n2. Указываете в какую валюту переводить.' \
      '\n3. Указываете количество, сколько переводить.' \
      '\n4. Проверяете введенные данные.' \
      '\nЧтобы ознакомиться со списком доступных валют напишите команду /help')


@bot.message_handler(commands=['help'])
def handle_start(message):
    key = keyboard()
    bot.send_message(message.chat.id, text=str(valute_dict).rstrip('}').lstrip('{'))


@bot.message_handler(commands=['convert'], func=lambda message: get_state_for_text(message) == valute)
def handle_start(message):
    key = keyboard()
    bot.send_message(message.chat.id, text='Напиши название в какую валюту переводить?', reply_markup=key)


@bot.message_handler( func=lambda message: get_state_for_text(message) == tovalute)
def handle_tovalute(message):
    key = keyboard()
    bot.send_message(message.chat.id, text='Напиши название из какой валюты переводить', reply_markup=key)


@bot.message_handler( func=lambda message: get_state_for_text(message) == nominal)
def handle_nominal(message):
    bot.send_message(message.chat.id, text='Напиши сколько переводить?')
    update_state_for_text(message, getter)


@bot.message_handler( func=lambda message: get_state_for_text(message) == getter)
def handle_getter(message):
    if check_float(message.text):
        buttons = noonekey()
        valute_list = get_valute(message.chat.id)
        update_valute(message.chat.id, 'nominal', message.text)
        bot.send_message(message.chat.id, text='Все верно \nПереводим из - {}?\n'
                                           'Переводим в {} \nКолличество {}'
                        .format(valute_dict.get(valute_list['tovalute']), 
                                valute_dict.get(valute_list['valute']), 
                                valute_dict.get(valute_list['nominal'])), reply_markup=
                        buttons)
        update_state_for_text(message, see)
    else:
        bot.send_message(message.chat.id, text='Кажется вы ввели не число')


@bot.message_handler( func=lambda message: get_state_for_text(message) == see)
def handle_see(message):
    if message.text == 'Да':
        bot.send_message(message.chat.id, text='result')
        valute_list = get_valute(message.chat.id)
        result = convertor(valute_list['tovalute'], valute_list['valute'], valute_list['nominal'])
        bot.send_message(message.chat.id, text='{} {} стоит {} {}'.format(valute_list['nominal'],
                                                                          prettyprint(str(valute_list['nominal']),
                                                                                      valute_list['tovalute']),
                                                                          *result,
                                                                          prettyprint(str(int(*result)), valute_list['valute'])))
        update_state_for_text(message, valute)
    else:
        key = again_button()
        bot.send_message(message.chat.id, text='Again', reply_markup=key)
        update_state_for_text(message, valute)


#                                             Секция для клавиатуры
@bot.callback_query_handler(func=lambda message: get_state(message) == valute)
def callback_query(query):
    key = onekey()
    message = query.message
    text = query.data
    bot.delete_message(query.message.chat.id, query.message.message_id)
    bot.answer_callback_query(query.id, 'Нажмите далее')
    update_valute(query.message.chat.id, 'valute', text)
    update_state(query, tovalute)
    bot.send_message(query.message.chat.id, b'\xF0\x9F\x91\x87', reply_markup=key)


@bot.callback_query_handler(func=lambda message: get_state(message) == tovalute)
def callback_query(query):
    key = onekey()
    message = query.message
    text = query.data
    bot.delete_message(query.message.chat.id, query.message.message_id)
    bot.answer_callback_query(query.id, 'Нажмите далее')
    update_valute(query.message.chat.id, 'tovalute', text)
    update_state(query, nominal)
    bot.send_message(query.message.chat.id, b'\xF0\x9F\x91\x87', reply_markup=key)


#                                             Секция для состояний
def update_state(message, state):
    user_state[message.message.chat.id] = state


def update_state_for_text(message, state):
    user_state[message.chat.id] = state


def get_state(message):
    return user_state[message.message.chat.id]


def get_state_for_text(message):
    return user_state[message.chat.id]


def update_valute(user_id, key, value):
    products[user_id][key] = value


def get_valute(message):
    return products[message]


def convertor(val, toval, nominal):
    val, toval, nominal = val.upper(), toval.upper(), float(nominal)
    mydict = {'RU': 1}
    url1 = 'http://www.cbr.ru/scripts/XML_daily.asp?'
    r = requests.get(url=url1)
    soup = BeautifulSoup(r.text, 'lxml')
    for tag in soup.find_all('valute'):
        mydict[tag.charcode.text] =  float((tag.value.text).replace(',', '.')) / int(tag.nominal.text)
    if (val in mydict.keys()) and (toval in mydict.keys()):
        return [(round((mydict[val] / mydict[toval]) * nominal, 2))]


def check_float(nominal):
    try:
        return (float(nominal))
    except ValueError:
        return

@server.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://trykeyboardbot.herokuapp.com/' + token)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))