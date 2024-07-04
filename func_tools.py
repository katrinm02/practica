from telebot.types import Message
from db import is_admin_from_db_by_id
import telebot
import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

bot = telebot.TeleBot(config["TelegramBot"]["token"])


def find_in_args(args, target_type):
    for arg in args:
        if isinstance(arg, target_type):
            return arg

def find_in_kwargs(kwargs, target_type):
    return find_in_args(kwargs.values(), target_type)

def get_message_info(*args, **kwargs):
    message_args = find_in_args(args, Message)
    if message_args is not None:
        return message_args.chat.id, message_args.text

    message_kwargs = find_in_kwargs(kwargs, Message)
    if message_kwargs is not None:
        return message_kwargs.chat.id, message_kwargs.text

    return "UNKNOWN", "UNKNOWN"

def no_access(message):
    bot.send_message(message.from_user.id, "низя(")

def admin_requered(func):
    def wrapper(*args, **kwargs):
        chat_id, text = get_message_info(*args, **kwargs)
        try:
            if is_admin_from_db_by_id(chat_id):
                func(*args, **kwargs)
            else:
                no_access(*args, **kwargs)
            print(
                f"[LOG] Finished {func.__name__} - chat_id {chat_id}",
                text
            )
        except Exception as e:
            print(
                f"[LOG] Failed {func.__name__} - chat_id {chat_id} - exception {e}"
            )

    return wrapper