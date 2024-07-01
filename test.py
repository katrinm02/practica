# import configparser  # импортируем библиотеку

# config = configparser.ConfigParser()  # создаём объекта парсера
# config.read("settings.ini")  # читаем конфиг

# print(config["TelegramBot"]["token"])  # обращаемся как к обычному словарю!
# # 'johndoe'

# ------------------
# import configparser
# import psycopg2

# config = configparser.ConfigParser()  # создаём объекта парсера
# config.read("settings.ini") 

# # Параметры подключения к базе данных PostgreSQL 
# # DATABASE = { 
# #     'dbname': 'grumming', 
# #     'user': 'postgres', 
# #     'password': '1234', 
# #     'host': 'localhost', 
# # } 

# DATABASE = { 
#         'dbname': config["DB"]["dbname"], 
#         'user': config["DB"]["user"], 
#         'password': config["DB"]["password"], 
#         'host': config["DB"]["host"], 
#     }

# connection = psycopg2.connect(**DATABASE) 
# cursor = connection.cursor() 
# cursor.execute("SELECT name, phone FROM phone_order") 
# result = cursor.fetchone() 
# print(result)
# cursor.close() 
# connection.close() 
# ------------
# import json
# a = [{"a":1, "b":2},{"a":1, "b":2}]
# a1 = json.dumps(a)
# print(a1)
# print(type(a1))
# a2 = json.loads(a1)
# print(a2)
# print(type(a2))
# print(type(a2[0]))
# # import time
# from datetime import datetime, timedelta
# print(type(time.time()))
# print(datetime.fromtimestamp(time.time()))
# print(datetime.fromtimestamp(1719855221))
# print(datetime.fromtimestamp(time.time()) - datetime.fromtimestamp(1719855221) > timedelta(minutes=2))

