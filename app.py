from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
import os

from main import (
    start,
    like,
    add_photo
)

app = Flask(__name__)

TOKEN = os.environ['TOKEN']
bot = Bot(TOKEN)


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return 'hi from Python-2022I'

    elif request.method == 'POST':
        data = request.get_json(force=True) # get data from request

        update: Update = Update.de_json(data, bot)
        print(update)

        dp: Dispatcher = Dispatcher(bot, None, workers=0)  # dispatcher   
        
        dp.add_handler(CommandHandler('start', callback=start))
        dp.add_handler(MessageHandler(Filters.photo, callback=add_photo))
        dp.add_handler(CallbackQueryHandler(callback=like))

        dp.process_update(update) # process update
        return 'hello'