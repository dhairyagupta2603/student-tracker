import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # keys
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'encrypted'

    # SQL configs
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'tracker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TESTING = False
