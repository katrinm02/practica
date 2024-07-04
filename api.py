import json
import string
import random
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from db import *
import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

app = FastAPI()

# Генерация номера заявки
def generate_ticket():
    letters = string.ascii_uppercase
    numbers = string.digits
    ticket = ''.join(random.choices(letters, k=3)) + ''.join(random.choices(numbers, k=3))
    return ticket

def post_notification(ticket):
    message_text = f"Зарегистрирована новая заявка!\nНомер заявки: {ticket}"
    requests.post(f"https://api.telegram.org/bot{config['TelegramBot']['token']}/sendMessage?chat_id={config['BotGroups']['work_chat']}&text={message_text}")

# Обработчик для отправки данных из формы в базу данных
@app.post("/api/v1/post_ticket", status_code=200, response_class=HTMLResponse)
async def post_ticket(name: str = Form(...), phone: str = Form(...)):
    ticket = generate_ticket()
    data =  post_data_from_site_to_db(name, phone, ticket)
    post_notification(ticket)


# Роут FastAPI для обработки запросов от телеграм бота (запрос по номеру заявки)
@app.get("/api/v1/get_order_info")
async def get_order_info(ticket: str):
    data = fetch_data_from_db_by_ticket(ticket)
    if data:
        name, phone, status_id, status, status_dt = data
        return {"name": name, "phone": phone, "status_id": status_id, "status": status, "status_dt": status_dt}
    else:
        return {"error": "Order not found"}

@app.get("/api/v1/close_ticket")
async def close_ticket(ticket: str):
    close_ticket_db(ticket)

# Роут FastAPI для обработки запросов от телеграм бота (запрос неотработанных заявок)
@app.get("/api/v1/get_undone_ticket")
async def get_undone_ticket():
    data = fetch_data_from_db_by_status(1)
    if data:
        data = list(map(lambda row: {"num": row[0], "name": row[1], "phone": row[2], "ticket": row[3]} , data))
        return json.dumps(data)
    else:
        return {"error": "Order not found"}