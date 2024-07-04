import json
from telebot import types, TeleBot
import requests
import configparser
from datetime import datetime, timedelta
from time import time

from func_tools import *

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

bot = TeleBot(config["TelegramBot"]["token"])
api_url = "http://127.0.0.1:8000/api/v1"

bot.set_my_commands(
   commands=[
      types.BotCommand('get_orders_to_phone', 'Получить заявки на звонки'),
      types.BotCommand('get_order_info', 'Получить информаицию по тикету'),
   ]
)

@bot.message_handler(commands = ['get_orders_to_phone'])
@admin_requered
def url(message):
    response = requests.get(f"{api_url}/get_undone_ticket")
    json_calls = response.json()
    if "error" in json_calls:
        bot.send_message(message.from_user.id, "Все заявки закрыты")
    else:
        calls = []
        for call in json.loads(json_calls):
            calls.append(f"""{call["num"]}) Заявка: {call["ticket"]},\n     Телефон: {call["phone"]},\n     Имя: {call["name"]}""")
        bot.send_message(message.from_user.id, "\n".join(calls))


@bot.message_handler(commands = ['get_order_info'])
@admin_requered
def url(message):
    bot.send_message(message.from_user.id, 'Отправьте номер заявки')
    bot.register_next_step_handler(message, get_ticket_number)

def get_ticket_number(message):
    ticket_number = message.text
    response = requests.get(f"{api_url}/get_order_info?ticket={ticket_number}")
    json_calls = response.json()
    if "error" in json_calls:
        bot.send_message(message.from_user.id, "Такой заявки нет")
    else:
        answer =  f"Имя: {json_calls['name']},\nТелефон: {json_calls['phone']},\nСтатус: {json_calls['status']}\nСтатус изменен: {json_calls['status_dt']}"
        dict_args = {
            'chat_id':message.chat.id,
            'text': answer
        }
        if json_calls['status_id'] == 1:
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Закрыть заявку", callback_data=f'edit_ticket={ticket_number}')
            button2 = types.InlineKeyboardButton("Закрыть окно", callback_data='close')
            for n in (button1,button2):
                markup.row(n)
            dict_args['parse_mode'] = 'html'
            dict_args['reply_markup'] = markup

        bot.send_message(**dict_args)


@bot.callback_query_handler(func=lambda callback: True)
# Поменял callback на call для удобности
def callback_query(call):
    if 'edit_ticket' in call.data:
        if datetime.fromtimestamp(time()) - datetime.fromtimestamp(call.message.date) > timedelta(minutes=2):
            bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
            bot.send_message(call.message.chat.id, "Сообщение уже не актуально. Пожалуйста отвечайте в течение двух минут")
        else:
            requests.get(f"{api_url}/close_ticket?ticket={call.data.split('=')[1]}")
            bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
            bot.send_message(call.message.chat.id, f"Заявка закрыта")
    if call.data == 'close':
        bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')

# Handle all other messages.
@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document',
    'text', 'location', 'contact', 'sticker'])
def default_command(message):
    bot.send_message(message.chat.id, "Пожалуйста введи комманду. Я тебя не понимаю(")

bot.polling(none_stop=True, interval=0)