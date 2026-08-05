"""WTForms used by public HTML pages."""

from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class BookingForm(FlaskForm):
    """Create a room reservation from the public booking page."""

    room_id = SelectField("Room", coerce=int, validators=[DataRequired()])
    guest_name = StringField(
        "Guest name",
        validators=[DataRequired(), Length(max=120)],
    )
    guest_email = StringField(
        "Guest email",
        validators=[DataRequired(), Email(), Length(max=255)],
    )
    starts_at = DateTimeLocalField(
        "Starts at",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()],
    )
    ends_at = DateTimeLocalField(
        "Ends at",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()],
    )
    submit = SubmitField("Book room")


class LoginForm(FlaskForm):
    """Admin login form."""

    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")
