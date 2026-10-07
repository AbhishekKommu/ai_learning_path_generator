from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, ValidationError
from backend.models import User


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 128)])
    confirm = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password", "Passwords must match.")])
    submit = SubmitField("Create account")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower().strip()).first():
            raise ValidationError("That email is already registered.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class GenerateForm(FlaskForm):
    goal = StringField("What do you want to become or learn?", validators=[DataRequired(), Length(3, 200)])
    level = SelectField("Your current level", choices=[("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced")])
    hours_per_week = IntegerField("Hours per week", default=5, validators=[DataRequired(), NumberRange(1, 60)])
    total_weeks = IntegerField("Weeks available", default=8, validators=[DataRequired(), NumberRange(2, 52)])
    interests = StringField("Interests or skills you already have (optional)", validators=[Length(0, 300)])
    submit = SubmitField("Generate my path")


class EditForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(3, 150)])
    notes = TextAreaField("Notes", validators=[Length(0, 1000)])
    submit = SubmitField("Save changes")


class ProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 80)])
    bio = TextAreaField("About you", validators=[Length(0, 300)])
    submit = SubmitField("Save profile")
