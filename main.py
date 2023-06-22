import flask_bootstrap
from flask import Flask, render_template, url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from smtplib import SMTP
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,length,Length
from wtforms import EmailField,SubmitField,PasswordField,TextAreaField,StringField,SearchField
from threading import Thread
from flask_bootstrap import Bootstrap
from os import environ




app = Flask(__name__)

Bootstrap(app)

db = SQLAlchemy()

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users-data.db'

class Email(FlaskForm):
    email = EmailField('Email',validators=[InputRequired(),length(min=1)])
    name = StringField('Name',validators=[InputRequired(),length(min=1)])
    subject = StringField('Subject',validators=[InputRequired(),length(min=1)])
    message = TextAreaField("Message",validators=[InputRequired(),Length(min=3)])
    submit = SubmitField('Send')


@app.route('/')
def home():

    return render_template('index.html')

@app.route('/contact',methods=['GET',"POST"])
def contact():
    if request.method == "GET":
        form = Email()
        return render_template('contact.html',form = form)
    else:
        try:
            with SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login('samuelwhitehall@gmail.com', environ["EMAIL_PASSWORD"])
                connection.sendmail(from_addr='samuelwhitehall@gmail.com',to_addrs='samuelwhitehall@gmail.com',msg=f"Subject:{request.form['subject']}\n\n Name: {request.form['name']} Email: {request.form['email']}  Message: {request.form['message']}")
            return render_template('success.html')
        except TimeoutError:
            return render_template('failed.html')
    
@app.route('/fiver')
def fiver():
    return render_template('fiver.html')

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html')



if __name__ == "__main__":

    app.run(debug = True)
