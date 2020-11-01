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


# https://python-telegram-bot.readthedocs.io/en/stable/telegram.user.html


def dog(update, context):
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        contents = requests.get('https://random.dog/woof.json').json()
        url = contents['url']
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    
    # TODO logging the user info: id, username, firstname and lastname
    # this way, the Raspberry Pi will comunicate its' ID only to you
    # and youìll be able to connect via SSH
    chat_id = update.message.chat_id
    logging.info('dog - chat_id: {} - user is bot: {}'.format(chat_id, is_bot))
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
                        level=logging.INFO,
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