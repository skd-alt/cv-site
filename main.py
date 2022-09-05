from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired
import os
import smtplib

app = Flask(__name__)
app.config['SECRET_KEY'] = "eoo5544yuui7899"

Bootstrap5(app)


class ContactForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        message = form.message.data

        my_email = os.environ.get("MYEMAIL")
        password = os.environ.get("EPASSWORD")

        with smtplib.SMTP(os.environ.get("SMTP")) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs=my_email,
                msg=f"Subject: Website Message\n\nName of Sender:{name}\n\n{message}"
            )

        return redirect("contact")
    return render_template("contact.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)