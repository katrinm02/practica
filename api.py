import json
from fastapi import FastAPI, Form 
from fastapi.responses import HTMLResponse 
# from telegram import Bot
import random 
import string
from db import *

# Генерируем номер заявки 
def generate_ticket(): 
    letters = string.ascii_uppercase 
    numbers = string.digits 
    ticket = ''.join(random.choices(letters, k=3)) + ''.join(random.choices(numbers, k=3)) 
    return ticket 
 
app = FastAPI() 
 
# # Обработчик для отправки данных из формы в базу данных 
# @app.post("/api/v1/post_ticket", status_code=200, response_class=HTMLResponse) 
# async def submit_form(name: str = Form(...), phone: str = Form(...)): 
#     connection = psycopg2.connect(**DATABASE) 
#     cursor = connection.cursor() 
#     ticket = generate_ticket() 
 
# # Вставляем данные из формы в базу данных 
#     cursor.execute("INSERT INTO phone_order (name, phone, ticket) VALUES (%s, %s, %s)", (name, phone, ticket)) 
#     connection.commit() 
#     cursor.close() 
#     connection.close() 
# # Отправка уведомления о заявке в Telegram 
#     TOKEN = '' 
#     bot = Bot(token=TOKEN) 
#     group_id = '' 
 
#     message_text = f'Зарегистирована новая заявка!\nНомер заявки: {ticket}' 
#     await bot.send_message(chat_id=group_id, text=message_text) 
 
#     return "<h2>Ваша заявка принята! Дождитесь звонка оператора." 
 
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