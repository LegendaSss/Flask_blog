from flask import Flask
from flask.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from core.config import Config


# Импортируем конфигурацию из модуля core.config


app = Flask(__name__)
# Создаем экземпляр Flask-приложения


# Применяем конфигурацию из объекта Config
app.config.from_object(Config)


db = SQLAlchemy(app)
# Инициализируем SQLAlchemy для работы с базой данных
migrate = Migrate(app, db)
# Инициализируем Flask-Migrate для управления миграциями базы данных


login_manager = LoginManager(app)
# Инициализируем Flask-Login для управления аутентификацией пользователей
login_manager.login_niew = 'login'
# Устанавливаем маршрут для входа пользователя


from core import routes, models
# Импортируем маршруты и модели из соответствующих модулей
