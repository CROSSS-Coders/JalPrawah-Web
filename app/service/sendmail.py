import requests
from app.setting import MAILGUN_KEY, MAILGUN_URL


def send_mail(to, subject, text):
    return requests.post(MAILGUN_URL,
                         auth=("api",  MAILGUN_KEY),
                         data={"from": "Flood Alert <mailgun@mg.pushpak1300.me>",
                               "to": to,
                               "subject": subject,
                               "text": text})
