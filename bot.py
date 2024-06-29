import json
import telebot
import requests
import configparser

from func_tools import *

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

bot = telebot.TeleBot(config["TelegramBot"]["token"])
api_url = "http://127.0.0.1:8000/api/v1"

bot.set_my_commands(
   commands=[
      telebot.types.BotCommand('get_orders_to_phone', 'Получить заявки на звонки'),
      telebot.types.BotCommand('get_order_info', 'Получить информаицию по тикету'),
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
        for call in json_calls:
            calls.append(f"""{call["num"]}) ticket: {call["ticket"]}, phone: {call["phone"]}, name: {call["name"]}""")
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
        answer =  f"Имя: {json_calls['name']},  Телефон: {json_calls['phone']}"
        bot.send_message(message.chat.id, answer)
    

# Handle all other messages.
@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document',
    'text', 'location', 'contact', 'sticker'])
def default_command(message):
    bot.send_message(message.chat.id, "Пожалуйста введи комманду. Я тебя не понимаю(")

bot.polling(none_stop=True, interval=0)

# @bot.message_handler(commands = ['start'])
# def url(message):
#     markup = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://habr.com/ru/all/')
#     markup.add(btn1)
#     bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на сайт хабра", reply_markup = markup)