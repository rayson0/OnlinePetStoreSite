from flask_wtf import FlaskForm  # подключаем базовый класс формы
# подключаем возможные поля
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, validators
# подключаем модули проверки
from wtforms.validators import DataRequired


# любая форма — это класс, унаследованный от FlaskForm
class LoginForm(FlaskForm):
    user = StringField("user", validators=[DataRequired()])  # текстовое поле с никнеймом
    grade = StringField("grade", validators=[DataRequired()])  # текстовое поле c оценкой
    text = TextAreaField("text", validators=[DataRequired()])  # описание отзыва
    submit = SubmitField()  # кнопка «отправить»


class LikeForm(FlaskForm):
    dislike = SubmitField()  # кнопка дизлайка


class RegistrationForm(FlaskForm):
    login = StringField("login", [DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField("password", [DataRequired(), validators.Length(min=4, max=25)])
    password_again = PasswordField("password", [DataRequired(), validators.Length(min=4, max=25)])
    submit = SubmitField()
