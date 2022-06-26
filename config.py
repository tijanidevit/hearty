import os


# basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'wait-go-ahead'
    # MYSQL_DATABASE_USER = "root"
    # MYSQL_DATABASE_PASSWORD = ""
    # MYSQL_DATABASE_DB = "heart_api"
    # MYSQL_DATABASE_HOST = "localhost"

    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'wait-go-ahead'
    MYSQL_DATABASE_USER = "b4e7b19361cd10"
    MYSQL_DATABASE_PASSWORD = "01c4f31a"
    MYSQL_DATABASE_DB = "heroku_f26f9dcab714203"
    MYSQL_DATABASE_HOST = "eu-cdbr-west-02.cleardb.net"

    # mysql://b4e7b19361cd10:01c4f31a@eu-cdbr-west-02.cleardb.net/heroku_f26f9dcab714203?reconnect=true