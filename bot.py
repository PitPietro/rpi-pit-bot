import os
import sys
import time
import random
import telepot
import datetime
from gpiozero import LED
from dotenv import load_dotenv
from os.path import join, dirname


#LED
def on():
    my_led.on()
    print('ON')
    return

def off():
    my_led.off()
    print('OFF')
    return


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    if command == '/on':
        bot.sendMessage(chat_id, on())
    elif command =='/off':
       bot.sendMessage(chat_id, off())
       


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
my_token = os.environ.get('MY_TOKEN')
print('token init')
my_led = LED(17)
print('LED init')
bot = telepot.Bot(my_token)
bot.message_loop(handle)
print('. . .')
print('I am listening...')

while 1:
     time.sleep(10)
