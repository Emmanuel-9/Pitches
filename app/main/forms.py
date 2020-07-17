from flask_wtf import FlaskForm
from wtforms import SelectField,TextAreaField,SubmitField,StringField
from wtforms.validators import Required

class PitchForm(FlaskForm):

  title = StringField('Pitch title')
  category = SelectField("Choose Category",choices=[('Brand','Personal brand'),('Product','Product'),('Project','Project'),('Investor','Investor')])
  pitch = TextAreaField('Your Pitch',validators=[Required()])
  submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
  bio =TextAreaField('Short description about you.',validators=[Required()])
  submit = SubmitField('Submit ')

class CommentForm(FlaskForm):
  comment = TextAreaField('Your Comment',validators=[Required()])
  submit = SubmitField('Submit')