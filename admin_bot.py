import os
import json
import telebot
import requests

from constants import DEV_PATH, DEV_PATH

DEBUG = os.getenv('FLASK_DEBUG', False)
PATH = DEV_PATH if DEBUG else DEV_PATH

TOKEN = os.getenv('POLESTAGEADMIN_TOKEN')
USER_TOKEN = os.getenv('POLESTAGE_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "привет от Админа")


@bot.message_handler(commands=['notification'])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Напишите объявление")
    bot.register_next_step_handler(message, send_notification)


def send_notification(message):
    notification = message.text
    chat_ids = []
    with open(f'{PATH}chat_ids.txt',"r", encoding="utf-8") as file:
        chat_ids = file.read().split("\n")
    for chat_id in chat_ids:
        if chat_id:
            url_req = f"https://api.telegram.org/bot{USER_TOKEN}/sendMessage?chat_id={chat_id}&text={notification}"
            results = requests.get(url_req)
            print(results.json())
    # bot.send_message('Обьявление отправлено');




def main() -> None:
    """Run the bot."""
    print("Admin Bot are running...")
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("notification", "Отправить объявление"),
        ],
    )

    bot.polling()

if __name__ == "__main__":
    main()
