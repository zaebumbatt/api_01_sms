import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

VK_TOKEN = os.getenv('VK_TOKEN')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')

URL = 'https://api.vk.com/method/users.get'
VERSION = 5.92

CLIENT = Client(TWILIO_SID, TWILIO_TOKEN)


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'v': VERSION,
        'access_token': VK_TOKEN,
        'fields': 'online',
    }
    try:
        response = requests.post(URL, params=params)
    except requests.exceptions.HTTPError:
        print('HTTP Error')
    except requests.exceptions.ConnectionError:
        print('Connecting Error')
    except requests.exceptions.Timeout:
        print('Timeout Error')
    except requests.exceptions.RequestException:
        print('Unknown Error')
    else:
        user_status = response.json().get('response')
        if user_status is None:
            print('User does not exist')
        else:
            return user_status[0]['online']


def sms_sender(sms_text):
    message = CLIENT.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO,
    )
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
