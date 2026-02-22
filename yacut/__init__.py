
from dotenv import load_dotenv

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config

load_dotenv()

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from . import error_handlers, models, views, api_views, yandex_disk