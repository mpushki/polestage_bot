import os
import json
import telebot
import datetime

from constants import RU_WEEK

TOKEN = '5666693511:AAE9GxOtjStnkyIJZ4RCG9B8ohCGm3RTg2E'
bot = telebot.TeleBot(TOKEN)

data = ""
with open('trainers.json',"r", encoding="utf-8") as file:
    data = json.load( file)


timetable = ""
with open('timetable.json',"r", encoding="utf-8") as file:
    timetable = json.load( file)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    with open('chat_ids.txt', 'r+') as file:
        content = file.read()
        if not str(message.chat.id) in content:
            file.write(f"{message.chat.id}\n")
    bot.send_message(message.chat.id, "Добро пожаловать в PoleStage")


@bot.message_handler(commands=['day'])
def get_text_messages(message):
    now = datetime.datetime.now()
    print(f"Today is {now}")
    today_timetable = timetable[now.strftime("%A")]
    bot.send_message(message.chat.id, f"Расписание на сегодня {now.strftime('%d.%m')}")
    text = '\n'.join(today_timetable)
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['week'])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Расписание на неделю")
    text = ""
    for day, time_of_day in timetable.items():
        ru_day = RU_WEEK[day]
        text += f"{ru_day}\n" + "\n".join(time_of_day) + "\n\n"
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
            kk = telebot.types.InlineKeyboardButton(text=trainer_data1["name"], callback_data=trainer1)
            keyboard.row(fff, kk)
        else:
            keyboard.row(fff)

    bot.send_message(message.chat.id, "Список:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if data.get(call.data, None): #call.data это callback_data, которую мы указали при объявлении кнопки
        trainer_data = data[call.data]
        bot.send_photo(call.message.chat.id, photo=open(f'assets/{trainer_data["image"]}.jpg', 'rb'))

        message = f"{trainer_data['name']}\n" \
                  f"Inst: {trainer_data['inst']}\n" \
                  f"Основные направления: {trainer_data['types']}\n\n" \
                  f"{trainer_data.get('description', '')}"

        bot.send_message(call.message.chat.id, message)



def main() -> None:
    """Run the bot."""
    print("Bot are running...")
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("week", "Расписание на неделю"),
            telebot.types.BotCommand("day", "Расписание на сегодня"),
            telebot.types.BotCommand("trainers", "Узнать о наших тренерах")
        ],
    )


    bot.infinity_polling(none_stop=True, interval=0)

if __name__ == "__main__":
    main()
