from flask import render_template, url_for, redirect, flash
from flask_login import current_user, logout_user, login_user, login_required
from movie_app import app
from movie_app.forms import MovieForm, RegistrationForm, LoginForm
from movie_app.models import Movie, db, User

@app.route('/', methods=["GET", "POST"])
def index():
    movies = Movie.query.all()
    form = MovieForm()
    if current_user.is_authenticated:
        user = User.query.filter(User.id == current_user.id).first()
        return render_template('index.html', form=form, movies=movies[-5:], user=user)
    else:
        user = None
        return render_template('index.html', form=form, movies=movies[-5:])

@app.route('/home')
def home():
    if current_user.is_authenticated:
        user = User.query.filter(User.id == current_user.id).first()
        return render_template('home.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/profile/<username>')
def user_profile(username):
    user = User.query.filter(User.username == username).first()
    if user:
        return render_template('user_profile.html', user=user)
    else:
        return "Такого пользователя не существует"

##### ---- REGISTRATION ----- #####
@app.route('/reg', methods=["GET", "POST"])
def reg():
    form = RegistrationForm()
    return render_template('reg.html', form=form)

@app.route('/process-reg', methods=["GET", "POST"])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        if not form.password_validation(form.password1.data, form.password2.data):
            flash("Пароли не совпадают")
            return redirect(url_for('reg'))
        if not form.username_validation(form.username.data):
            flash("Пользователь с таким логином уже существует")
            return redirect(url_for('reg'))
        User.create_user(username=form.username.data, password=form.password1.data)
        flash("Вы успешно зарегистрировались")
        return redirect(url_for('login'))
    else:
        flash("Вы что-то не заполнили")
        return redirect(url_for('reg'))


##### ---- LOGIN ----- #####
@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form = LoginForm()
        return render_template('login.html', form=form)


@app.route('/process-login', methods=["GET", "POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.validate_login(form.username.data, form.password.data):
            user = User.query.filter(User.username == form.username.data).first()
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Неправильный логин или пароль")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Разлогинено')
    return redirect(url_for('index'))


@app.route('/add-movie',  methods=["GET", "POST"])
def add_movie():
    movie = MovieForm()
    new_movie = Movie.query.filter(Movie.title == movie.title.data).first()
    if current_user.is_authenticated:
        user = User.query.filter(User.id == current_user.id).first()
        if not new_movie:
            User.add_movie(
                title=movie.title.data, about=movie.comment.data, user=user)
            flash("Ваш фильм добавлен")
            return redirect(url_for('index'))
        else:
            flash("Такой фильм уже есть")
            return redirect(url_for('index'))
    else:
        if not new_movie:
            m = Movie(title=movie.title.data, about=movie.comment.data)
            db.session.add(m)
            db.session.commit()
            flash("Ваш фильм добавлен")
            return redirect(url_for('index'))
        else:
            flash("Такой фильм уже есть")
            return redirect(url_for('index'))



