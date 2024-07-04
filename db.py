import configparser
import psycopg2

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

DATABASE = {
        'dbname': config["DB"]["dbname"],
        'user': config["DB"]["user"],
        'password': config["DB"]["password"],
        'host': config["DB"]["host"],
    }

# Параметры подключения к базе данных PostgreSQL
def get_db():
    connection = psycopg2.connect(**DATABASE)
    return connection.cursor(), connection

def close_db(cursor, connection):
    cursor.close()
    connection.close()


# Добавление данных из формы в бд
def post_data_from_site_to_db(name, phone, ticket):
    cursor, connection = get_db()
    cursor.execute("""
                   INSERT INTO phone_order (name, phone, ticket, status_id) VALUES (%s, %s, %s, %s)""", (name, phone, ticket, 1))
    connection.commit()
    close_db(cursor, connection)

# Получение данных из базы по ticket
def fetch_data_from_db_by_ticket(ticket):
    cursor, connection = get_db()
    cursor.execute("""
                   SELECT
                        po.name,
                        po.phone,
                        s.id as status_id,
                        s."name" as status,
                        TO_CHAR(case
                            when s.id = 1 then po.receive_dt
                            else po.ready_dt
                        end,'YYYY-MM-DD HH24:MI:SS') as status_dt
                    FROM phone_order po
                    join status s on s.id = po.status_id
                    WHERE ticket = %s""", (ticket,))
    result = cursor.fetchone()
    close_db(cursor, connection)
    return result

def close_ticket_db(ticket):
    cursor, connection = get_db()
    cursor.execute("""
                   update phone_order
                    set status_id = 2, ready_dt=now()
                    WHERE ticket = %s""", (ticket,))
    connection.commit()
    close_db(cursor, connection)

# Получение данных из базы данных по статусу
def fetch_data_from_db_by_status(status_id):
    cursor, connection = get_db()
    cursor.execute("SELECT row_number() over(), name, phone, ticket FROM phone_order WHERE status_id = %s ORDER BY receive_dt", (status_id,))
    result = cursor.fetchall()
    close_db(cursor, connection)
    return result

# Получение роли сотрудника
def is_admin_from_db_by_id(id):
    cursor, connection = get_db()
    cursor.execute("""select 1 as result from "user" us join user_role ur on ur.id = us.role_id where us.id = %s and ur."role" = 'Администратор'""", (id,))
    result = cursor.fetchone()
    close_db(cursor, connection)
    return result != None