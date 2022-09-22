import telebot
import json


bot = telebot.TeleBot('5666693511:AAE9GxOtjStnkyIJZ4RCG9B8ohCGm3RTg2E')


data = ""
with open('trainers.json',"r", encoding="utf-8") as file:
    data = json.load( file)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # bot.reply_to(message, "Добро пожаловать")
    bot.send_message(message.chat.id, "Добро пожаловать")
    

@bot.message_handler(commands=['day'])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Рассписание на сегодня")


@bot.message_handler(commands=['trainers'])
def get_text_messages(message):
    keyboard = telebot.types.InlineKeyboardMarkup(); #наша клавиатура
    for trainer, trainer_data in data.items():
        print(trainer)
        # trainer_data = data[trainer]
        key = telebot.types.InlineKeyboardButton(text=trainer_data["name"], callback_data=trainer); #кнопка «Да»
        keyboard.add(key); #добавляем кнопку в клавиатуру

    bot.send_message(message.chat.id, "Список:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if data.get(call.data, None): #call.data это callback_data, которую мы указали при объявлении кнопки
        trainer_data = data[call.data]
        print(trainer_data)
        bot.send_photo(call.message.chat.id, photo=open(f'assets/{trainer_data["image"]}.jpg', 'rb'))
        bot.send_message(call.message.chat.id, trainer_data['name'] + "," + trainer_data['inst'] + "," + trainer_data['types'])
        


def main() -> None:
    """Run the bot."""
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("week", "Рассписание на неделю"),
            telebot.types.BotCommand("day", "Рассписание на сегодня"),
            telebot.types.BotCommand("trainers", "Узнать о наших трененрах")
        ],
        # scope=telebot.types.BotCommandScopeChat(12345678)  # use for personal command for users
        # scope=telebot.types.BotCommandScopeAllPrivateChats()  # use for all private chats
    )


    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
