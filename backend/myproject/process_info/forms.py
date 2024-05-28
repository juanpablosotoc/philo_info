from wtforms import StringField, SubmitField, FileField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL    


class ProcessInfoForm(FlaskForm):
    text = StringField(validators=[DataRequired()])
    link = StringField(validators=[DataRequired(), URL()])
    file = FileField()
    submit = SubmitField()
