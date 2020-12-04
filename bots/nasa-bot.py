import logging
import os
import time
import sys
from datetime import datetime
from os.path import join, dirname
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import nasapy
import urllib.request
from gtts import gTTS
from dotenv import load_dotenv

from telegram.ext import Updater, CommandHandler, Filters
import requests

date = datetime.today().strftime('%Y-%m-%d')
nasa = nasapy.Nasa

IMG_DIR = '../nasa_images'
AUDIOS_DIR = '../nasa_audios'

global_updater = Updater

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


def text_to_speech(msg, name):
    """
    @param msg the string message to convert in .mp3
    @param name the file name with which the file is saved
    """
    desc_obj = gTTS(text=msg, lang='en', slow=False)
    desc_obj.save(name)


def help_def(update, context):
    msg = '/pod send the photo of the day\n' \
          '/hd_pod send the photo of the day\n' \
          '/help print this message\n'
    update_user_info(update)
    log_info('help', update.message.message_id)
    context.bot.send_message(chat_id=user_info['id'], text=msg)


def folder_check_():
    # check if the image directory already exists (if not, then create it)
    dir_res = os.path.exists(IMG_DIR)
    if not dir_res:
        os.makedirs(IMG_DIR)

    # check if the audios directory already exists (if not, then create it)
    dir_res = os.path.exists(AUDIOS_DIR)
    if not dir_res:
        os.makedirs(AUDIOS_DIR)


def pod_def(update, context):
    update_user_info(update)
    log_info('pod', update.message.message_id)

    # get the image data:
    pod = nasa.picture_of_the_day(date=date, hd=True)

    # check the media type
    if pod['media_type'] == 'image':
        caption = '{} - © by {}'.format(pod['title'], pod['copyright'])
        context.bot.send_photo(chat_id=user_info['id'], photo=pod['url'], caption=caption)

    else:
        msg = 'Media type is not an image!\n I\'m sorry, NASA was hacked with HTML, try /pod later :confused:'
        context.bot.send_message(chat_id=user_info['id'], text=msg)


def hd_pod_def(update, context):
    update_user_info(update)
    log_info('hd_pod', update.message.message_id)

    # TODO fix this code: telegram.error.BadRequest: Wrong file identifier/http url specified
    # get the image data:
    pod = nasa.picture_of_the_day(date=date, hd=True)

    # check the media type
    if pod['media_type'] == 'image':
        caption = '{} - © by {}'.format(pod['title'], pod['copyright'])
        context.bot.send_document(chat_id=user_info['id'], document=pod['hdurl'], caption=caption)

    else:
        msg = 'Media type is not an image!\n I\'m sorry, NASA was hacked with HTML, try /pod later :confused:'
        context.bot.send_message(chat_id=user_info['id'], text=msg)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        filename='../log_bot.log',
        level=logging.INFO,
        datefmt='%d/%m/%Y %H:%M:%S')
    logging.info('Starting bot')

    dotenv_path = join(dirname(__file__), '../.env')
    load_dotenv(dotenv_path)
    nasa_key = os.environ.get('NASA_KEY')
    my_token = os.environ.get('MY_TOKEN')

    updater = Updater(my_token, use_context=True)
    dp = updater.dispatcher

    global global_updater, nasa
    global_updater = updater

    # create a Nasa object
    nasa = nasapy.Nasa(key=nasa_key)

    handlers = [CommandHandler('pod', pod_def), CommandHandler('hd_pod', hd_pod_def), CommandHandler('help', help_def)]

    for hs in handlers:
        dp.add_handler(hs)

    # Starts the bot, and the bot begins to start polling Telegram for any chat updates.
    updater.start_polling()

    # Block the script until you sends a command to break from the Python script (Ctrl + C)
    updater.idle()


if __name__ == '__main__':
    main()

# reference: https://www.educative.io/blog/how-to-use-api-nasa-daily-image
