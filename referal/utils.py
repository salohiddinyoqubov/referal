import os
import random
import string

import requests
from decouple import config


def generate_invite_code():
    letters_and_digits = string.ascii_uppercase + string.digits
    invite_code = ''.join(random.choices(letters_and_digits, k=8))
    return invite_code


def generate_otp_code():
    otp_code = ''.join(random.choices(string.digits, k=4))
    return otp_code


def send_sms(phone_number, otp_code):
    base_url = "https://api.infobip.com/sms/2/text/single"
    headers = {
        "Authorization": f"App {config('SMS_API')}",
        "Content-Type": "application/json"
    }

    message = f"Your activation code: {otp_code}"

    payload = {
        "from": "+998972800809",  # Replace with your sender ID or phone number
        "to": phone_number,
        "text": message
    }

    try:
        response = requests.post(base_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("OTP message sent successfully!")
        else:
            print(f"Failed to send OTP message. Status code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
