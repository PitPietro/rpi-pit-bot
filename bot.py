import os
import sys
import time
import random
# import telepot
import datetime
# from gpiozero import LED
from dotenv import load_dotenv
from os.path import join, dirname

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
# from telegram.ext.dispatcher import run_async
import requests
import re

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def dog(update, context):
    url = get_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url, caption="Dog caption")

def help(update, context):
    #chat_id = update.message.chat_id
    pass


def main():
    print('Start listening . . .')

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    my_token = os.environ.get('MY_TOKEN')

    updater = Updater(my_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('dog',dog))
    #dp.add_handler(CommandHandler('help',help))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()