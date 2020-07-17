from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import Required,EqualTo,Email
from ..models import User
    

class RegistrationForm(FlaskForm):
    email = StringField('Your email address', validators = [Required(),Email()])
    username = StringField('Enter your name',validators =[Required(),Email()])
    password = PasswordField('Enter a password of choice',validators = [Required(),EqualTo('password_confirm', message = 'Password must match')])
    password_confirm = PasswordField('Confirm password', validators = [Required()])
    submit = SubmitField('Sign Up')
 
    def validate_email(self,email_data): 
        if User.query.filter_by(email = data.field.data).first(): 
            raise ValidationError('There is an account with that email')

    def validate_username(self,username_data):
        if User.query.filter_by(username = data.field.data).first():
            raise ValidationError('That username is already taken')    


class LoginForm(FlaskForm):
    email = StringField('Your email address', validators = [Required()])
    password = PasswordField('Enter your password', validators = [Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')   