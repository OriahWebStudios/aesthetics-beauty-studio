from flask import url_for, render_template, current_app
from app import mail
from flask_mail import Message
import os
import hashlib
from urllib.parse import urlencode
import urllib
import config

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.sender = os.environ.get('MAIL_DEFAULT_SENDER')
    msg.html = render_template(template, **kwargs)
    mail.send(msg)

    