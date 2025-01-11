from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField, DateTimeField, FileField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import ServiceTable

class BookingForm(FlaskForm):
    full_name = StringField('Full Name *', validators=[DataRequired(message='First name is required')])
    email = StringField('Email *', validators=[DataRequired(message='Email is required'), Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message='Invalid email address')])
    cell_number = StringField('Cell Number *', validators=[DataRequired(message='Cell number is required'), Regexp(r'^\d{10}$', message='Please enter a valid 10-digit cell number')])
    selected_service = SelectField('Select Service *', choices=[], coerce=str)
    date = StringField('Choose Prefered Date *', validators=[DataRequired(message='Prefered date is requred')])
    time = StringField('Choose Prefered Date *', validators=[DataRequired(message='Prefered time is requred')])
    submit = SubmitField('Next')

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.selected_service.choices = [(service.id, f'{service.name} - R{service.price}') for service in ServiceTable.query.all()]