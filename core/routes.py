from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import (
    logout_user, current_user, login_required, login_user
)
from sqlalchemy.exc import SQLAlchemyError
from core.models import User, Post, Comment, LikeDislike
from core import app, db
from core.forms import RegForm, PostForm, LikeForm, DislikeForm, CommentForm


# Главная страница
@app.route('/')
def index():
    return render_template("index.html")


# Страница всех постов
@app.route('/posts')
def posts():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template("posts.html", posts=posts)


# Страница деталей поста и комментариев
@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    # Получаем пост по его ID
    post = Post.query.get_or_404(post_id)
    # Получаем комментарии для данного поста
    comments = Comment.query.filter_by(post_id=post.id).all()
    # Создаем формы для комментариев, лайков и дизлайков
    comment_form = CommentForm()
    like_form = LikeForm()
    dislike_form = DislikeForm()
    # Получаем количество лайков и дизлайков для поста
    post_likes = LikeDislike.query.filter_by(post_id=post.id,
                                             is_like=True).count()
    post_dislikes = LikeDislike.query.filter_by(post_id=post.id,
                                                is_like=False).count()
    return render_template("post_detail.html", post=post, comments=comments,
                           comment_form=comment_form, like_form=like_form,
                           dislike_form=dislike_form, post_likes=post_likes,
                           post_dislikes=post_dislikes)


# Обработчик добавления комментария к посту
@app.route('/posts/<int:post_id>/add_comment', methods=['POST'])
def add_comment(post_id):
    if request.method == 'POST':
        comment_content = request.form.get('comment_content')
        if comment_content:
            post = Post.query.get_or_404(post_id)
            # Создаем новый комментарий и добавляем его в базу данных
            comment = Comment(name=current_user.email,
                              content=comment_content, post=post)
            db.session.add(comment)
            db.session.commit()
            flash('Комментарий успешно добавлен!', 'success')
        else:
            flash('Пустой комментарий не допускается!', 'danger')
    return redirect(url_for('post_detail', post_id=post_id))


# Обработчик удаления комментария к посту
@app.route('/posts/<int:post_id>/delete_comment/'
           '<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(post_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.name == current_user.email:
        # Удаляем комментарий из базы данных,
        # если он принадлежит текущему пользователю
        db.session.delete(comment)
        db.session.commit()
        flash('Комментарий успешно удален!', 'success')
    else:
        flash('Вы не можете удалить этот комментарий!', 'danger')
    return redirect(url_for('post_detail', post_id=post_id))


# Обработчик удаления поста
@app.route('/posts/<int:id>/delete')
def post_delete(id):
    post = Post.query.get_or_404(id)
    try:
        # Удаляем пост из базы данных
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Ошибка при удалении поста: {str(e)}"


# Обработчик обновления поста
@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def post_update(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        # Обновляем данные поста в базе данных
        post.title = form.title.data
        post.content = form.content.data
        try:
            db.session.commit()
            flash('Пост успешно обновлен!', 'success')
            return redirect(url_for('post_detail', post_id=post.id))
        except Exception as e:
            db.session.rollback()
            flash(f'При обновлении поста произошла ошибка: {e}', 'danger')
    return render_template('post_update.html', form=form, post=post)


# Обработчик добавления нового поста
@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if request.method == 'POST':
        # Создаем новый пост и добавляем его в базу данных
        post = Post(title=form.title.data,
                    content=form.content.data,
                    user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('post.html', form=form)


# Обработчик выхода из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Обработчик регистрации нового пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegForm()
    if request.method == 'POST':
        # Создаем нового пользователя и добавляем его в базу данных
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Обработчик входа пользователя в систему
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Ошибка')
    return render_template('login.html')


# Обработчик лайка поста
@app.route('/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    existing_like = LikeDislike.query.filter_by(user_id=current_user.id,
                                                post_id=post.id,
                                                is_like=True).first()
    if not existing_like:
        # Если пользователь еще не поставил лайк этому посту,
        # создаем новый лайк и сохраняем в базу данных
        new_like = LikeDislike(user_id=current_user.id,
                               post_id=post.id, is_like=True)
        db.session.add(new_like)
        db.session.commit()
        flash('Пост понравился!', 'success')
    else:
        flash('Вы уже поставили лайк этому посту.', 'danger')
    return redirect(url_for('post_detail_without_comments', post_id=post_id))


# Обработчик дизлайка поста
@app.route('/posts/<int:post_id>/dislike', methods=['POST'])
@login_required
def dislike_post(post_id):
    post = Post.query.get_or_404(post_id)
    existing_dislike = LikeDislike.query.filter_by(user_id=current_user.id,
                                                   post_id=post.id,
                                                   is_like=False).first()
    if not existing_dislike:
        # Если пользователь еще не поставил дизлайк этому посту,
        # создаем новый дизлайк и сохраняем в базу данных
        new_dislike = LikeDislike(user_id=current_user.id,
                                  post_id=post.id, is_like=False)
        db.session.add(new_dislike)
        db.session.commit()
        flash('Пост не понравился!', 'success')
    else:
        flash('Вы уже поставили дизлайк этому посту.', 'danger')
    return redirect(url_for('post_detail_without_comments', post_id=post_id))


# Обработчик страницы деталей поста без комментариев
@app.route('/posts/<int:post_id>')
def post_detail_without_comments(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail_without_comments.html', post=post)
