import os
import telebot

TOKEN = os.getenv('POLESTAGEADMIN_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(441266876, "привет от Админа")

@bot.message_handler(content_types=['text'])
def get_messages(message):
    pass



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
