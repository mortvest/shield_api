import os
basedir = os.path.abspath(os.path.dirname(__file__))

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


class Config(object):
    POSTGRES_URL = get_env_variable("POSTGRES_URL")
    POSTGRES_USER = get_env_variable("POSTGRES_USER")
    POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
    POSTGRES_DB = get_env_variable("POSTGRES_DB")
    DB_URL = ('postgresql+psycopg2://{user}:{pw}@{url}/{db}'.
              format(user=POSTGRES_USER,
                     pw=POSTGRES_PASSWORD,
                     url=POSTGRES_URL,
                     db=POSTGRES_DB))
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = get_env_variable("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
    # JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
