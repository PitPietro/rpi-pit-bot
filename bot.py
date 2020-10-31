import os
import re
import sys
import time
import random
import logging
import datetime
import requests
from dotenv import load_dotenv
from os.path import join, dirname
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

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
    logging.info('dog - chat_id: {}'.format(chat_id))
    context.bot.send_photo(chat_id=chat_id, photo=url, caption="Dog caption")


def meme(update, context):
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        contents = requests.get('https://some-random-api.ml/meme').json()
        url = contents['image']
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    
    chat_id = update.message.chat_id
    logging.info('meme - chat_id: {}'.format(chat_id))
    context.bot.send_photo(chat_id=chat_id, photo=url, caption="Enjoy a meme")

def help(update, context):
    '''
    /dog
    /meme
    '''
    #chat_id = update.message.chat_id
    pass


def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        filename='log_bot.log',
                        level=logging.DEBUG,
                        datefmt='%d/%m/%Y %H:%M:%S')
    
    logging.info('Starting bot')

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    my_token = os.environ.get('MY_TOKEN')

    updater = Updater(my_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('dog',dog))
    dp.add_handler(CommandHandler('meme',meme))
    #dp.add_handler(CommandHandler('help',help))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()