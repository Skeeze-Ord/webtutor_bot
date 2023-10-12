import telebot
import psycopg2

connection = psycopg2.connect(
    database='answers',
    user='postgres',
    password='root',
    host='localhost',
    port=5432
)
cursor = connection.cursor()

# bot key
TOKEN = '6294705740:AAFRerVokBR-XTZu2GtBs0hbKpyg3hx9GEA'
bot = telebot.TeleBot(TOKEN)

users_greated = set()


@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    chat_id = message.chat.id

    if chat_id not in users_greated:
        bot.send_message(chat_id, "Привет! Напиши запрос который хочешь найти.")
        users_greated.add(chat_id)

    response = message.text
    query = f"SELECT title, description, url FROM handbook WHERE title LIKE '%{response}%'"

    cursor.execute(query)
    results = cursor.fetchall()

    if results:
        for row in results:
            title, description, url = row
            response_message = f"<b>{title}</b>\n\n" \
                               f"<i>{description}</i>\n\n" \
                               f"Ссылка на документ: {url}"
            bot.send_message(message.chat.id, response_message, parse_mode='HTML')
    elif response[0] == '/':
        bot.send_message(message.chat.id, "Незвестная команда.")
    else:
        bot.send_message(message.chat.id, "Ничего не найдено.")


bot.polling()

cursor.close()
connection.close()
