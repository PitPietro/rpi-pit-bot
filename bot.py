# import sys
# import time
# import random
import logging
import os
import re
import subprocess
from os.path import join, dirname

# import datetime
import requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

allowed_extension = ['jpg', 'jpeg', 'png']

# https://python-telegram-bot.readthedocs.io/en/stable/telegram.user.html
user_info = {'id': 0, 'username': '', 'first_name': '', 'last_name': ''}
bot_info = {'id': 0, 'token': '', 'name': '', 'username': '', 'first_name': '', 'last_name': '', 'link': '',
            'commands': ''}


def update_user_info(update):
    # chat_id = update.message.chat_id
    # user_id must be equal to chat_id
    user_obj = update.message.from_user
    user_info['id'] = user_obj.id
    user_info['username'] = user_obj.username
    user_info['first_name'] = user_obj.first_name
    user_info['last_name'] = user_obj.last_name


def update_bot_info(my_bot):
    """
    @param my_bot `context.bot` from any handler `context`
    """
    # token = context.bot.token
    bot_info['id'] = my_bot.id
    bot_info['token'] = my_bot.token
    bot_info['name'] = my_bot.name
    bot_info['username'] = my_bot.username
    bot_info['first_name'] = my_bot.first_name
    bot_info['last_name'] = my_bot.first_name
    bot_info['link'] = my_bot.link
    bot_info['commands'] = my_bot.commands


def log_info(msg_type, msg_id, msg=''):
    """
    @param msg_type where the log start from (dog, info, ip, ...)
    @param msg_id ID of the message
    @param msg optional message to log
    """

    if msg != '':
        msg = ' - message: ' + msg + ' - '
    logging.info('{} - message id: {}{} ~ Sender ~ id: {} - username: {} - first name: {} - last name: {}'
                 .format(msg_type, msg_id, msg, user_info['id'], user_info['username'], user_info['first_name'],
                         user_info['last_name']))


def log_bot():
    logging.info(
        '~ Bot info ~ id: {} - token: {} - name: {} - username: {} - first name: {} - last name: {} - links: {} - '
        'commands: {}'.format(bot_info['id'], bot_info['token'], bot_info['name'], bot_info['username'],
                              bot_info['first_name'], bot_info['last_name'], bot_info['link'], bot_info['commands']))


def dog(update, context):
    file_extension = ''
    while file_extension not in allowed_extension:
        contents = requests.get('https://random.dog/woof.json').json()
        url = contents['url']
        file_extension = re.search("([^.]*)$", url).group(1).lower()

    chat_id = update.message.chat_id
    msg_id = update.message.message_id

    update_user_info(update)
    log_info('dog', msg_id)

    context.bot.send_photo(chat_id=chat_id, photo=url, caption="Dog caption")


def meme(update, context):
    file_extension = ''
    while file_extension not in allowed_extension:
        contents = requests.get('https://some-random-api.ml/meme').json()
        url = contents['image']
        file_extension = re.search("([^.]*)$", url).group(1).lower()

    chat_id = update.message.chat_id
    msg_id = update.message.message_id

    update_user_info(update)
    log_info('dog', msg_id)
    context.bot.send_photo(chat_id=chat_id, photo=url, caption="Enjoy a meme")


def help_msg(update, context):
    """
    /dog
    /meme
    /ip
    /info
    """
    # chat_id = update.message.chat_id

    msg = '/dog send a dog photo\n' \
          '/info send the user info\n' \
          '/ip send the local IP of the machine where the bot runs\n' \
          '/meme send a meme photo\n'
    update_user_info(update)
    log_info('help', update.message.message_id)
    context.bot.send_message(chat_id=user_info['id'], text=msg)


def send_ip(update, context):
    data = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
    my_ip = str(data.communicate())
    my_ip = my_ip.split('\n')
    my_ip = my_ip[0].split('\\')

    res = []
    for line in my_ip:
        res.append(line)
    my_ip = res[0][3:]

    update_bot_info(context.bot)
    log_bot()

    chat_id = update.message.chat_id

    update_user_info(update)
    log_info('ip', update.message.message_id)
    context.bot.send_message(chat_id=chat_id, text='My local IP is: {}'.format(my_ip))


def info(update, context):
    update_user_info(update)
    log_info('info', update.message.message_id)

    msg = 'Hi {}! Your name is {} {} and your ID is {}'.format(
        user_info['username'], user_info['first_name'], user_info['last_name'], user_info['id'])
    context.bot.send_message(chat_id=user_info['id'], text=msg)


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
    dp.add_handler(CommandHandler('help', help_msg))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
