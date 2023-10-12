import telebot
import psycopg2
import os

db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")

connection = psycopg2.connect(
    database=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)
cursor = connection.cursor()

# bot key
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

users_greated = set()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    if chat_id not in users_greated:
        bot.send_message(chat_id, "Привет! Напиши запрос который хочешь найти.")
        users_greated.add(chat_id)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    response = message.text
    if len(response) < 2:
        bot.send_message(chat_id, "Введите запрос чуть точнее")
    else:
        response = response.replace(" ", "|")

        query = f"SELECT title, description, url FROM handbook WHERE title ~* '({response})'"

        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            for row in results:
                title, description, url = row
                response_message = f"<b>{title}</b>\n\n" \
                                   f"<i>{description}</i>\n\n" \
                                   f"Ссылка на документ: {url}"
                bot.send_message(chat_id, response_message, parse_mode='HTML')
        elif response[0] == '/':
            bot.send_message(chat_id, "Незвестная команда.")
        else:
            bot.send_message(chat_id, "Ничего не найдено.")


bot.polling()

cursor.close()
connection.close()
