from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo

from movie_app.models import User, db


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=25)])
    submit = SubmitField("Войти")

    def validate_login(self, username, password):
        user = User.query.filter(User.username == username).first()
        if user:
            if user.password == password:
                return True
        return False

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=25)])
    password1 = PasswordField("Password1", validators=[DataRequired(), Length(min=4, max=25)])
    password2 = PasswordField("Password2", validators=[DataRequired(), Length(min=4, max=25)])
    submit = SubmitField("Зарегистрироваться")

    def password_validation(self, password1, password2):
        if not password1 == password2:
            return False
        return True

    def username_validation(self, username):
        user = User.query.filter(User.username == username).count()
        if user:
            return False
        return True
        


class MovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    comment = TextAreaField("Comment", validators=[Length(max=150)])
    submit = SubmitField("Поделиться")

