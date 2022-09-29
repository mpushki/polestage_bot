import os
import json
import time
import logging
import telebot
import datetime
from flask import Flask, request


logging.basicConfig(format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)

from models import Bot
from constants import RU_WEEK, PROD_PATH, DEV_PATH, WEB_APP

DEBUG = os.getenv('FLASK_DEBUG', False)
PATH = DEV_PATH if DEBUG else PROD_PATH
user_bot = Bot(PATH)

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
        # Telegram can repeat update if get any status except 200
        # Need check update_id to ignore repeated updates
        update_id = update.update_id
        with open(f'{PATH}update_id.txt', 'r+') as file:
            content = file.read()
            if not update_id == content:
                file.seek(0)
                file.write(str(update_id))
                file.truncate()

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
    keyboard = telebot.types.InlineKeyboardMarkup() # create a new keyboard with all trainers
    iter_trainers = iter(trainers.items())
    for trainer_id, trainer_data in iter_trainers:
        key = telebot.types.InlineKeyboardButton(text=trainer_data["name"], callback_data=trainer_id)
        next_trainer = next(iter_trainers, None)
        if next_trainer:
            # To show all trainers for 2 columns
            next_trainer_id, next_trainer_data = next_trainer
            second_key = telebot.types.InlineKeyboardButton(text=next_trainer_data["name"], callback_data=next_trainer_id)
            keyboard.row(key, second_key)
        else:
            keyboard.row(key)

    bot.send_message(message.chat.id, "Наши тренера:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if trainers.get(call.data, None):
        trainer_data = trainers[call.data]
        bot.send_photo(call.message.chat.id, photo=open(f'{PATH}assets/{trainer_data["image"]}.jpg', 'rb'))

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

