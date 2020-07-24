import os

#получаем путь к нашему файлу
basedir = os.path.abspath(os.path.dirname(__file__))

#указываем где хотим, чтобы находился файл cstudio.db
#директория запускаемого файла(basedir) и на одну директорию выше(..)
# sqlite:/// нужен для того, чтоьбы дать понять, какой тип бд мы хотим использовать
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "movies.db")
# sqlite:/// нужен для того, чтоьбы дать понять, какой тип бд мы хотим использовать
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = '784ggfrdjbdf9wfidsc8e'

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'