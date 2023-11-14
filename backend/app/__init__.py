import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, 
                  db, 
                  render_as_batch=os.environ.get('MIGRATE_RENDER_AS_BATCH'))

from app import routes, models