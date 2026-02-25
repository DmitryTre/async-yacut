import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_YaCUT',
        default='sqlite:///yacut_v1_dev.db'
    )
    SECRET_KEY = os.getenv('SECRET_KEY', default='some_secret_key')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
    YA_CUT_BASE_PATH = 'ya_cut/'
