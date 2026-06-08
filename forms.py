from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField, IntegerField,
                            DateField, RadioField, SelectField,
                            SubmitField)
from wtforms.validators import DataRequired, equal_to, length
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed


class RegisterForm(FlaskForm):

    username = StringField("Enter Username", validators=[
        DataRequired()
    ])
    password = PasswordField("Enter Password", validators=[
        DataRequired(),
        length(min=6, max=24),
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        equal_to("password", message="პაროლები არ ემთხვევა")
    ])


    register = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()

    login = SubmitField("Log In")


class BookForm(FlaskForm):
    image = FileField("Upload Book Cover")
    title = StringField("Enter Book Title")
    author = StringField("Enter Author Name")
    
    submit = SubmitField("Save Book")
