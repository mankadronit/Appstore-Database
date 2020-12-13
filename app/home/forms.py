from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, InputRequired


class DeveloperForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    website = StringField('Website', validators=[DataRequired()])
    bank_acc_number = IntegerField('Bank Account Number', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ApplicationForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    package_name = StringField('Package Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    app_type = SelectField('App Type', validators=[DataRequired()], 
                               choices = [('Free', 'Free'), ('Paid', 'Paid'), ('Sub', 'Sub')])

    price = FloatField('Price', validators=[InputRequired(), NumberRange(min=0, max=1000)])
    submit = SubmitField('Submit')