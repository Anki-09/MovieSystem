from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,PasswordField,BooleanField,SubmitField,FloatField
from wtforms.validators import DataRequired,Length,ValidationError,Email,EqualTo,NumberRange
from app.models import User
class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember_me=BooleanField('Keep me logged in')
    submit=SubmitField('Sign In')
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField( 'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
         user = User.query.filter_by(username=username.data).first()
         if user is not None:
             raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('email address is already used by an existing account.')
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
class ReviewForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    rate = FloatField('Rate out of 10', validators=[DataRequired(), NumberRange(min=0,max=10,message='rate should be between 0 to 10')])
    submit = SubmitField('Submit')
