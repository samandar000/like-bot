from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import os
import requests

TOKEN = os.environ['TOKEN']
chennal_username = '@like_test_122313'


def start(update: Update, context: CallbackContext):
    update.message.reply_text('welcome to bot')


def add_photo(update: Update, context: CallbackContext):
    # get photo id form photo
    photo_id = update.message.photo[-1].file_id
    r = requests.post('https://djdev001.pythonanywhere.com/api/add-img/', json={"photo_id": photo_id})

    data = r.json()
    doc_id = data.get('doc_id')
    if doc_id:
        bot = context.bot
        btns = [
            [
                InlineKeyboardButton(text=f'👍:{0}', callback_data=f'like:{doc_id}'), 
                InlineKeyboardButton(text=f'👎:{0}', callback_data=f'dislike:{doc_id}')
            ]
        ]
        bot.send_photo(
            chat_id=chennal_username, 
            photo=photo_id,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns))



def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.photo, add_photo))

    updater.start_polling()
    updater.idle()

main()