import os
import json
import time
import telebot
import datetime
from flask import Flask, request
app = Flask(__name__)

from constants import RU_WEEK, PROD_PATH, DEV_PATH, WEB_APP

DEBUG = os.getenv('FLASK_DEBUG', False)
PATH = DEV_PATH if DEBUG else PROD_PATH

TOKEN = os.getenv('POLESTAGE_TOKEN')
bot = telebot.TeleBot(TOKEN, threaded=False)
secret = "GUIDtest"

# Get data
# To Do: Moved to DB
trainers = ""
with open(f'{PATH}trainers.json',"r", encoding="utf-8") as file:
    trainers = json.load( file)

timetable = ""
with open(f'{PATH}timetable.json',"r", encoding="utf-8") as file:
    timetable = json.load( file)
# End getting data

bot.remove_webhook() # need if web app will be releaded
time.sleep(1)
bot.set_webhook(url=f"{WEB_APP}{secret}", max_connections=1)

@app.route(f'/{secret}', methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
    return "ok", 200


@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open(f'{PATH}chat_ids.txt', 'r+') as file:
        content = file.read()
        if not str(message.chat.id) in content:
            # Saving chart _ids to send info notifications for all users
            file.write(f"{message.chat.id}\n")
    welcome_message = 'Добро пожаловать в PoleStage \U0001F60A\n\n'\
    'Здесь вы можете получить актуальную инфомацию о расписании и наших тренерах, '\
    'а также получать моментальные нотификации о заменах, акциях и мероприятиях студии.'

    bot.send_message(message.chat.id, welcome_message)


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
    jjj = iter(trainers.items())
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
    if trainers.get(call.data, None): #call.data это callback_data, которую мы указали при объявлении кнопки
        trainer_data = trainers[call.data]
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

if __name__ == "__main__":
    main()
    app.run()

