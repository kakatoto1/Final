from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, EmailField, PasswordField, FileField
from wtforms.validators import InputRequired, Length, DataRequired
from wtforms.widgets import TextArea, PasswordInput


class DeleteForm(FlaskForm):
    username = StringField("Username")
    confirm = SubmitField("Confirm")


class AddForm(FlaskForm):
    username = EmailField(validators=[DataRequired()],
                          render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Password"})

    about = StringField(validators=[InputRequired(), Length(min=10, max=100)], widget=TextArea(),
                        render_kw={"placeholder": "About"})
    submit = SubmitField("Submit")


class EditForm(AddForm):
    username = EmailField(validators=[DataRequired()],
                          render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[DataRequired()],
                             widget=PasswordInput(hide_value=False),
                             render_kw={"placeholder": "Password"})

    about = StringField(validators=[DataRequired()], widget=TextArea(),
                        render_kw={"placeholder": "About", "rows": 10})
    submit = SubmitField("Submit")


class UploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField("Upload")


class RegisterForm(FlaskForm):
    username = EmailField(validators=[DataRequired()],
                          render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    about = StringField(validators=[DataRequired()], widget=TextArea(),
                        render_kw={"placeholder": "About"})


class LoginForm(FlaskForm):
    username = EmailField(validators=[DataRequired()],
                          render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")
