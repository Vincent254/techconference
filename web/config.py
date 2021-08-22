import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    DEBUG = True
    POSTGRES_URL = "techconfdb.postgres.database.azure.com"  # TODO: Update value
    POSTGRES_USER = "surambaya@techconfdb"  # TODO: Update value
    POSTGRES_PW = "@cloudy2021"  # TODO: Update value
    POSTGRES_DB = "techconfdb"  # TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'ds+4PvFwXqL3YDLhbGBBxs8cEHfuqEms+TjHn9EXcdc='
    SERVICE_BUS_CONNECTION_STRING = 'Endpoint=sb://gotta-servicebus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=ds+4PvFwXqL3YDLhbGBBxs8cEHfuqEms+TjHn9EXcdc='  # TODO: Update value
    SERVICE_BUS_QUEUE_NAME = 'notificationqueue'
    ADMIN_EMAIL_ADDRESS = 'vmwagiru@gmail.com'
    SENDGRID_API_KEY = 'kkkk'  # Configuration not required, required SendGrid Account


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
