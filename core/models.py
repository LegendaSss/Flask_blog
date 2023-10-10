from flask_login import UserMixin
from datetime import datetime
from core import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Модель пользователя с наследованием от UserMixin для поддержки Flask-Login
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # Поле для электронной почты пользователя
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Поле для пароля пользователя
    password = db.Column(db.String(60), nullable=False)
    # Отношение пользователь - посты
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'
    # Представление объекта пользователя при выводе


# Модель поста
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    # Заголовок поста
    title = db.Column(db.String(100), nullable=False)
    # Содержание поста
    content = db.Column(db.String(300), nullable=False)
    # Дата и время создания поста
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # Внешний ключ на пользователя
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Отношение пост - комментарии
    comments = db.relationship('Comment', backref='post', lazy=True)
    # Отношение пост - лайки/дизлайки
    likes_dislikes = db.relationship('LikeDislike', backref='post', lazy=True)

    def __repr__(self):
        return f'<Post {self.title}>'
    # Представление объекта поста при выводе


# Модель комментария
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    # Имя автора комментария
    name = db.Column(db.String(100), nullable=False)
    # Содержание комментария
    content = db.Column(db.String(300), nullable=False)
    # Дата и время создания комментария
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # Внешний ключ на пост
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.name}>'
    # Представление объекта комментария при выводе


# Модель для лайков и дизлайков к постам
class LikeDislike(db.Model):
    __tablename__ = 'likes_dislikes'
    id = db.Column(db.Integer, primary_key=True)
    # Внешний ключ на пользователя
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Внешний ключ на пост
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    # Флаг для обозначения лайка (True) или дизлайка (False)
    is_like = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Post {self.user_id}>'
    # Представление объекта лайка/дизлайка при выводе
