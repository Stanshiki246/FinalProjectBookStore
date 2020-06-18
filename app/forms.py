from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.Users import Users
from app.models.Products import Products

class MultipleCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name=StringField('First Name',validators=[DataRequired()])
    last_name=StringField('Last Name',validators=[DataRequired()])
    phone_num=StringField('Phone Number',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        StringArr=list(username.data)
        found=False
        for char in StringArr:
            if char == '<' or char == ',' or char == "." or char == "\'" or char == "\"" or char == ">" or char == "/" or char == ";":
                found=True
                break
        if found:
            raise ValidationError('Cannot use regular expression')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        StringArr=list(email.data)
        found=False
        for char in StringArr:
            if char == '<' or char == ',' or char == "/" or char == "\'" or char == "\"" or char == ">" or char == ";":
                found=True
                break
        if found:
            raise ValidationError('Cannot use regular expression')

    def validate_phone_num(self,phone_num):
        user = Users.query.filter_by(phone_number=phone_num.data).first()
        if user is not None:
            raise ValidationError('Please use a different phone number.')
        DigitArr=['0','1','2','3','4','5','6','7','8','9']
        StringArr=list(phone_num.data)
        found=False
        for char in StringArr:
            if char not in DigitArr:
                found=True
                break
        if found:
            raise ValidationError('Must use number')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_num=StringField('Phone Number',validators=[DataRequired()])
    oldpassword=PasswordField('Old Password',validators=[DataRequired()])
    newpassword = PasswordField('New Password', validators=[DataRequired()])
    newpassword2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('newpassword')])
    submit = SubmitField('Save')

    def validate_username(self, username):
        StringArr=list(username.data)
        found=False
        for char in StringArr:
            if char == '<' or char == ',' or char == "." or char == "\'" or char == "\"" or char == ">" or char == "/" or char == ";":
                found=True
                break
        if found:
            raise ValidationError('Cannot use regular expression')

    def validate_email(self, email):
        StringArr=list(email.data)
        found=False
        for char in StringArr:
            if char == '<' or char == ',' or char == "/" or char == "\'" or char == "\"" or char == ">" or char == ";":
                found=True
                break
        if found:
            raise ValidationError('Cannot use regular expression')

    def validate_phone_num(self,phone_num):
        DigitArr=['0','1','2','3','4','5','6','7','8','9']
        StringArr=list(phone_num.data)
        found=False
        for char in StringArr:
            if char not in DigitArr:
                found=True
                break
        if found:
            raise ValidationError('Must use number')



class AddProduct(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    bookTypes = RadioField('Book Type',validators=[DataRequired()],choices=[('Comic','Comic'),('Novel','Novel')])
    image = FileField('Cover Book',validators=[DataRequired()])
    genreList=["Romance","School","Action","Sci-Fi","Comedy","Fantasy","Slice of Life","Mecha","Harem","Horror","Mystery",
               "Drama"]
    genreChoices=[(i,i) for i in genreList]
    genres=MultipleCheckboxField('Genres',validators=[DataRequired()],choices=genreChoices)
    synopsis=TextAreaField('Synopsis',validators=[DataRequired()])
    author=StringField('Author',validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_title(self,title):
        product=Products.query.filter_by(title=title.data).first()
        if product is not None:
            raise ValidationError('Please use a different username.')
        StringArr=list(title.data)
        found=False
        for char in StringArr:
            if char == '<' or char == ',' or char == "." or char == "\'" or char == "\"" or char == ">" or char == "/" or char == ";":
                found=True
                break
        if found:
            raise ValidationError('Cannot use regular expression')

    def validate_synopsis(self,synopsis):
        StringArr=list(synopsis.data)
        found=False
        for char in StringArr:
            if char == '<' or char == "/" or char == "\'" or char == "\"" or char == ">" or char == ";":
                found=True
                break
        if found:
            raise ValidationError('Cannot use regular expression')

    def validate_author(self,author):
        StringArr=list(author.data)
        found=False
        for char in StringArr:
            if char == '<' or char == "/" or char == "\'" or char == "\"" or char == ">" or char == ";":
                found=True
                break
        if found:
            raise ValidationError('Cannot use regular expression')


class PageJump(FlaskForm):
    page=IntegerField('Pages',validators=[DataRequired()])
    submit=SubmitField('Jump To')

class SearchTitle(FlaskForm):
    title=StringField('Search Title',validators=[DataRequired()])
    submit=SubmitField('Search')

    def validate_title(self,title):
        StringArr=list(title.data)
        found=False
        for char in StringArr:
            if char == '<' or char == ',' or char == "." or char == "\'" or char == "\"" or char == ">" or char == "/" or char == ";":
                found=True
                break
        if found:
            raise ValidationError('Cannot use regular expression')

class AddComicPage(FlaskForm):
    filename=MultipleFileField('Page Files',validators=[DataRequired()])
    submit=SubmitField('Add')

class EditProducts(FlaskForm):
    genreList=["Romance","School","Action","Sci-Fi","Comedy","Fantasy","Slice of Life","Mecha","Harem","Horror","Mystery",
               "Drama"]
    genreChoices=[(i,i) for i in genreList]
    genres=MultipleCheckboxField('Genres',validators=[DataRequired()],choices=genreChoices)
    synopsis=TextAreaField('Synopsis',validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_synopsis(self,synopsis):
        StringArr=list(synopsis.data)
        found=False
        for char in StringArr:
            if char == '<' or char == "/" or char == "\'" or char == "\"" or char == ">" or char == ";":
                found=True
                break
        if found:
            raise ValidationError('Cannot use regular expression')

class PaymentProofForm(FlaskForm):
    bank_account_name=StringField('Bank Account Owner',validators=[DataRequired()])
    bank_name=StringField('Bank Name',validators=[DataRequired()])
    exact_price=IntegerField('Exact Amount of Transferred Money',validators=[DataRequired()])
    hours=IntegerField('Transfer Time',validators=[DataRequired()])
    minutes=IntegerField(':',validators=[DataRequired()])
    submit=SubmitField('Send',validators=[DataRequired()])

    def validate_bank_account_name(self,bank_account_name):
        StringArr=list(bank_account_name.data)
        found=False
        for char in StringArr:
            if char == '<' or char == ',' or char == "." or char == "\'" or char == "\"" or char == ">" or char == "/" or char == ";":
                found=True
                break
        if found:
            raise ValidationError('Cannot use regular expression')

    def validate_bank_name(self,bank_name):
        StringArr=list(bank_name.data)
        found=False
        for char in StringArr:
            if char == '<' or char == ',' or char == "." or char == "\'" or char == "\"" or char == ">" or char == "/" or char == ";":
                found=True
                break
        if found:
            raise ValidationError('Cannot use regular expression')

    def validate_exact_price(self,exact_price):
        DigitArr=['0','1','2','3','4','5','6','7','8','9']
        StringArr=list(str(exact_price.data))
        found=False
        for char in StringArr:
            if char not in DigitArr:
                found=True
                break
        if found:
            raise ValidationError('Must use number')

    def validate_hours(self,hours):
        DigitArr=['0','1','2','3','4','5','6','7','8','9']
        StringArr=list(str(hours.data))
        found=False
        for char in StringArr:
            if char not in DigitArr:
                found=True
                break
        if found:
            raise ValidationError('Must use number')

        if hours.data < 0 or hours.data > 23:
            raise ValidationError('Cannot exceed between 0 and 23')

    def validate_minutes(self,minutes):
        DigitArr=['0','1','2','3','4','5','6','7','8','9']
        StringArr=list(str(minutes.data))
        found=False
        for char in StringArr:
            if char not in DigitArr:
                found=True
                break
        if found:
            raise ValidationError('Must use number')

        if minutes.data < 0 or minutes.data > 59:
            raise ValidationError('Cannot exceed between 0 and 59')
