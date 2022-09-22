from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,ValidationError
from wtforms.validators import DataRequired,Email,EqualTo
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField,FileAllowed
from my_portfolio_website.models import User
from flask_login import current_user

class RegisterForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired(),EqualTo("pass_confirm",message="密碼必須相同!")])
    username=StringField("Username",validators=[DataRequired()])
    pass_confirm=PasswordField("Confirm password",validators=[DataRequired()])
    submit=SubmitField("Register")

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("信箱已被使用過")

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username已被使用過")

class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired(),Email()])
    submit=SubmitField("Log in")


class UpdateUserForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    username=StringField("Username",validators=[DataRequired()])
    picture=FileField("Update profile picture",validators=[FileAllowed("jpg","png")])
    submit=SubmitField("Update")

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("信箱已被使用過")

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username已被使用過")

class CommentForm(FlaskForm):
    comment_text=CKEditorField("Comment",validators=[DataRequired()])
    submit=SubmitField("Submit Comment")