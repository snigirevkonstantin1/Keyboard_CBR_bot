import telebot
from collections import defaultdict
from numisfloat import check_float
from convert import convertor
from prettynominal import prettyprint
from different_keyboard import keyboard, noonekey, onekey, again_button
import os
from flask import Flask, request
from telebot import apihelper
import time #(for local start bot)


# section for variables
token = '1012225068:AAGMQCpQ7XJ8z2wg_pD42T2MdO97nHI_L7k'
bot = telebot.TeleBot(token)
user_state = defaultdict(lambda: valute)
products = defaultdict(lambda: {})
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
valute, tovalute, nominal, getter, see = range(5)
server = Flask(__name__)


# Command handler
@bot.message_handler(commands=['start'])
def handle_start(message):
    key = keyboard()
    bot.send_message(message.chat.id, text='Здравствуйте. \n Данный бот выполняет функции калькулятора валют. '
                                           'Данные берутся c сайта центра банка РФ на сегодняшнею дату. '
                                           'В зависимости от количества валюты бот пытается склонять ответное сообщение.'
                                           '\nРабота с ботом: для калькулятора валют напишите команду /convert ' \
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
    bot.send_message(message.chat.id, text='Укажите название из какой валюты переводить?', reply_markup=key)


@bot.message_handler( func=lambda message: get_state_for_text(message) == tovalute)
def handle_tovalute(message):
    key = keyboard()
    bot.send_message(message.chat.id, text='Укажите название в какую валюту переводить', reply_markup=key)


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
                        .format(valute_dict.get(valute_list['valute']),
                                valute_dict.get(valute_list['tovalute']),
                                message.text), reply_markup=
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
                                                                                      valute_list['valute']),
                                                                          *result,
                                                                          prettyprint(str(int(*result)), valute_list['tovalute'])))
        update_state_for_text(message, valute)
    else:
        key = again_button()
        bot.send_message(message.chat.id, text='Again', reply_markup=key)
        update_state_for_text(message, valute)


#    Section for a keyboard

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


#    Section for condition
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


#                                         Start local bot
("""
try:
    bot.polling(none_stop=True, interval=0,timeout=20)
except Exception as e:
    print(e.args)
    time.sleep(2)
    """)


# weebhook
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