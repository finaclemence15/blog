from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,ValidationError,SelectField
from wtforms.validators import Required,Email
from ..models import User, Subscription

class CommentForm(FlaskForm):

    # title = StringField('Review title',validators=[Required()])
    username=StringField('Username', validators = [Required()])
    comment = TextAreaField('Blog comment', validators=[Required()])
    submit = SubmitField('Submit')
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class AddBlogForm(FlaskForm):
    title=StringField('Title', validators = [Required()])
    content = TextAreaField ('Blog', validators = [Required()])
    submit = SubmitField('SUBMIT')

class SubscriptionForm(FlaskForm):
   name=StringField('Name',validators =[Required()])
   email=StringField('Email',validators =[Required()])
   submit = SubmitField('Submit')
   def validate_email(self,data_field):
            if Subscription.query.filter_by(email =data_field.data).first():
                raise ValidationError('we already have an account here')

class UpdateBlogForm(FlaskForm):
   title=StringField('Title',validators = [Required()])
   content=TextAreaField('Content',validators = [Required()])
   submit=SubmitField('SUBMIT')
