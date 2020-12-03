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

# reference: https://www.educative.io/blog/how-to-use-api-nasa-daily-image

if __name__ == '__main__':
    start_time = time.time()
    dotenv_path = join(dirname(__file__), '../.env')
    load_dotenv(dotenv_path)
    nasa_key = os.environ.get('NASA_KEY')

    # create a Nasa object
    nasa = nasapy.Nasa(key=nasa_key)

    # get today's date in YYYY-MM-DD format
    date = datetime.today().strftime('%Y-%m-%d')

    # get the image data:
    apod = nasa.picture_of_the_day(date=date, hd=True)

    # check the media type
    if apod['media_type'] == 'image':

        # display HD images only
        if 'hdurl' in apod.keys():
            # save name for the image
            image_title = date + "_" + apod['title'].replace(' ', '_').replace(':', '_') + '.jpg'

            # make a reference to the images directory and check if it already exists (if not, then create it)
            image_dir = '../nasa_images'
            dir_res = os.path.exists(image_dir)
            if not dir_res:
                os.makedirs(image_dir)

            # make a reference to the audios directory and check if it already exists (if not, then create it)
            audios_dir = '../nasa_audios'
            dir_res = os.path.exists(audios_dir)
            if not dir_res:
                os.makedirs(audios_dir)

            # retrieve the image
            urllib.request.urlretrieve(url=apod['hdurl'], filename=os.path.join(image_dir, image_title))

            # display info about the image
            for key in apod:
                print('{}\t{}'.format(key, apod[key]))

            # display the image
            image = mpimg.imread(os.path.join(image_dir, image_title))
            imgplot = plt.imshow(image)
            print('|--- {} seconds ---|'.format(time.time() - start_time))
            plt.show()

            # text to speech conversion
            image_desc = apod['explanation']
            desc_obj = gTTS(text=image_desc, lang='en', slow=False)
            audio_title = date + '_' + apod['title'] + '.mp3'
            desc_obj.save(os.path.join(audios_dir, audio_title))
            audio_file = os.path.join(audios_dir, audio_title)
            # play the mp3

    else:
        print('The media type is not an image')
