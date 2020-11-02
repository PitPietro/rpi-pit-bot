import os
import re
import sys
import time
import random
import logging
import datetime
import requests
import subprocess
from dotenv import load_dotenv
from os.path import join, dirname
from telegram.ext import Updater, InlineQueryHandler, CommandHandler


# https://python-telegram-bot.readthedocs.io/en/stable/telegram.user.html


def dog(update, context):
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        contents = requests.get('https://random.dog/woof.json').json()
        url = contents['url']
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    
    # the Raspberry Pi will communicate its' ID only to you
    # and you'll be able to connect via SSH (no need of screen)

    chat_id = update.message.chat_id
    msg_id = update.message.message_id
    user_obj = update.message.from_user
    user_id = user_obj.id
    user_username = user_obj.username
    user_first_name = user_obj.first_name
    user_last_name = user_obj.last_name

    # user_id must be equal to chat_id

    logging.info('dog - message id: {} ~ Sender ~ id: {} - username: {} - first name: {} - last name: {}'
                 .format(msg_id, user_id, user_username, user_first_name, user_last_name))
    context.bot.send_photo(chat_id=chat_id, photo=url, caption="Dog caption")


def meme(update, context):
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        contents = requests.get('https://some-random-api.ml/meme').json()
        url = contents['image']
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    
    chat_id = update.message.chat_id
    logging.info('meme - chat_id: {}'.format(chat_id))
    context.bot.send_photo(chat_id=chat_id, photo=url, caption="Enjoy a meme")


def help_msg(update, context):
    """
    /dog
    /meme
    """
    # chat_id = update.message.chat_id
    pass


def send_ip(update, context):
    data = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
    my_ip = str(data.communicate())
    my_ip = my_ip.split('\n')
    my_ip = my_ip[0].split('\\')

    res = []
    for line in my_ip:
        res.append(line)
    my_ip = res[0][3:]

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text='My local IP is: {}'.format(my_ip))

    print("local IP is: ", my_ip)


def info(update, context):
    user_obj = update.message.from_user
    user_id = user_obj.id
    user_username = user_obj.username
    user_first_name = user_obj.first_name
    user_last_name = user_obj.last_name

    msg = 'Hi {}! Your name is {} {} and your ID is {}'.format(user_username, user_first_name, user_last_name, user_id)
    context.bot.send_message(chat_id=user_id, text=msg)


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
    dp.add_handler(CommandHandler('dog', dog))
    dp.add_handler(CommandHandler('meme', meme))
    dp.add_handler(CommandHandler('ip', send_ip))
    dp.add_handler(CommandHandler('info', info))
    # dp.add_handler(CommandHandler('help',help_msg))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
