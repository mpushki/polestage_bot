import telebot


TOKEN = '5466837268:AAHYvFC7IMhKiWVUUmEE-mslIopx1D-hwTI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(441266876, "привет от Админа")

@bot.message_handler(content_types=['text'])
def get_messages(message):
    pass

bot.polling()