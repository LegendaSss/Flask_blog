from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     TextAreaField,
                     SubmitField)


from wtforms.validators import DataRequired, Email, EqualTo


# Форма для регистрации нового пользователя
class RegForm(FlaskForm):
    email = StringField('email', validators=[
        DataRequired(message='Это поле обязательное!'),
        Email(message='Некорректный формат email-адреса')
    ])
    password = PasswordField('пароль', validators=[
        DataRequired(message='Это поле обязательное!')
    ])
    confirm_password = PasswordField('проверка пароля', validators=[
        DataRequired(),
        EqualTo('password', message='Пароли должны совпадать')
    ])


# Форма для создания нового поста
class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[
        DataRequired(message='Это поле обязательное!')])
    content = TextAreaField('Описание', validators=[
        DataRequired(message='Это поле обязательное!')])
    # Поменял тут  PasswordField на TextAreaField и импортировал его...
    # Для многострочных текстовых полей!


# Форма для лайка поста
class LikeForm(FlaskForm):
    submit = SubmitField('Нравится')


# Форма для дизлайка поста
class DislikeForm(FlaskForm):
    submit = SubmitField('Не нравится')


# Форма для добавления комментария к посту
class CommentForm(FlaskForm):
    comment_content = TextAreaField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')
