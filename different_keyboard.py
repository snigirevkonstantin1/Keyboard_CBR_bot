from telebot import types

currensi = ['RU', 'AUD', 'AZN', 'GBP', 'AMD', 'BYN', 'BGN', 'BRL',
            'HUF', 'HKD', 'DKK', 'USD', 'EUR', 'INR', 'KZT',
            'CAD', 'KGS', 'CNY', 'MDL', 'NOK', 'PLN', 'RON',
            'XDR', 'SGD', 'TJS', 'TRY', 'TMT', 'UZS', 'UAH',
            'CZK', 'SEK', 'CHF', 'ZAR', 'KRW', 'JPY']


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