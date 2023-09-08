from json import dump

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import Users, Devices


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=50)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=2, max=50), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = Users.query.filter_by(e_mail=email.data).first()
        if user:
            raise ValidationError("Email already in use")


def validate_device(form, field):
    print(str(form))
    print(str(field.data))
    device = Devices.query.filter_by(device_platform=field.data).first()
    print("device" + str(device))
    if device:
        raise ValidationError(f"Device for {field.data} already exists")


class AddDevice(FlaskForm):
    choices = ['Web', 'Android', 'iOS']
    device_id = HiddenField()
    device_name = StringField("Device Name", validators=[DataRequired()])
    #device_platform = StringField("Device Platform", validators=[DataRequired()])
    device_platform = SelectField("Device Platform", coerce=str, choices=choices, validators=[DataRequired(), validate_device])
    user_id = HiddenField()
    submit = SubmitField("Add Device")
