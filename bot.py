import telebot
import json
import datetime


bot = telebot.TeleBot('5666693511:AAE9GxOtjStnkyIJZ4RCG9B8ohCGm3RTg2E')


data = ""
with open('trainers.json',"r", encoding="utf-8") as file:
    data = json.load( file)


timetable = ""
with open('timetable.json',"r", encoding="utf-8") as file:
    timetable = json.load( file)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # bot.reply_to(message, "Добро пожаловать")
    bot.send_message(message.chat.id, "Добро пожаловать в PoleStage")


@bot.message_handler(commands=['day'])
def get_text_messages(message):
    now = datetime.datetime.now()
    print(now)
    today_timetable = timetable[now.strftime("%A")]
    bot.send_message(message.chat.id, f"Расписание на сегодня {now.strftime('%d.%m')}")
    text = '\n'.join(today_timetable)
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['week'])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Расписание на неделю")
    text = ""
    for day, time_of_day in timetable.items():
        text += f"{day}\n" + "\n".join(time_of_day) + "\n\n"
    bot.send_message(message.chat.id, text)



@bot.message_handler(commands=['trainers'])
def get_text_messages(message):
    keyboard = telebot.types.InlineKeyboardMarkup(); #наша клавиатура
    keys = []
    jjj = iter(data.items())
    for trainer, trainer_data in jjj:
        fff = telebot.types.InlineKeyboardButton(text=trainer_data["name"], callback_data=trainer)
        fdfdfd = next(jjj, None)
        if fdfdfd:
            trainer1, trainer_data1 = fdfdfd
            print(trainer1, trainer_data1)
            kk = telebot.types.InlineKeyboardButton(text=trainer_data1["name"], callback_data=trainer1)
            keyboard.row(fff, kk)
        else:
            keyboard.row(fff)
        # index = list(data.keys()).index(trainer)
        # print(index)
        # if index % 2 == 1:
        #     keyboard.row(*keys)
        #     keys = []
        # key = telebot.types.InlineKeyboardButton(text=trainer_data["name"], callback_data=trainer)
        # keys.append(key)
        # print(keys)

        # keyboard.add(key); #добавляем кнопку в клавиатуру

    bot.send_message(message.chat.id, "Список:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if data.get(call.data, None): #call.data это callback_data, которую мы указали при объявлении кнопки
        trainer_data = data[call.data]
        print(trainer_data)
        bot.send_photo(call.message.chat.id, photo=open(f'assets/{trainer_data["image"]}.jpg', 'rb'))
        bot.send_message(call.message.chat.id, trainer_data['name'] + ", " + trainer_data['inst'] + ", " + trainer_data['types'])
        


def main() -> None:
    """Run the bot."""
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("week", "Расписание на неделю"),
            telebot.types.BotCommand("day", "Расписание на сегодня"),
            telebot.types.BotCommand("trainers", "Узнать о наших тренерах")
        ],
        # scope=telebot.types.BotCommandScopeChat(12345678)  # use for personal command for users
        # scope=telebot.types.BotCommandScopeAllPrivateChats()  # use for all private chats
    )


    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
