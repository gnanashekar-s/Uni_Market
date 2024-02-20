from flask import Flask , render_template ,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,ValidationError
from flask_login import UserMixin , LoginManager,logout_user,login_required,login_user,current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SECRET_KEY'] ="this is a secret key"

db = SQLAlchemy(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(20),nullable=False)
    lastname = db.Column(db.String(20),nullable=False)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(120),nullable=False)

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',validators=[InputRequired(),Length(min=4,max=20)])
    lastname = StringField('Last Name',validators=[InputRequired(),Length(min=1,max=20)])
    username = StringField('Username',validators=[InputRequired(),Length(min=4,max=20)])
    email = StringField('Email',validators=[InputRequired(),Length(min=8,max=40)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=20)])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken')
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(),Length(min=4,max=20)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=20)])
    submit = SubmitField('Login')  
@app.route('/')
def home():
    return render_template('landing_page.html')

@app.route('/login.html',methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form = form)


@app.route('/signup.html', methods=['GET','POST'])
def signup():
    form = RegistrationForm()
    
    return render_template('signup.html',form = form)


if __name__ == '__main__':
    app.run(debug=True)
    
