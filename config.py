import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQL_ALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQL_ALCHEMY_TRACK_MODIFICATIONS')
    PAYFAST_MERCHANT_ID = os.getenv('PAYFAST_MERCHANT_ID')
    PAYFAST_MERCHANT_KEY = os.getenv('PAYFAST_MERCHANT_KEY')
    PAYFAST_PASSPHRASE = os.getenv('PAYFAST_PASSPHRASE')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = "Oriah Web Studios, ramotsepanem@gmail.com"