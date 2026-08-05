"""WTForms used by public HTML pages."""

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateTimeLocalField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


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


class RoomForm(FlaskForm):
    """Create or edit a meeting room."""

    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    capacity = IntegerField(
        "Capacity",
        validators=[DataRequired(), NumberRange(min=1, max=1000)],
    )
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save room")
