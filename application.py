from flask import Flask, render_template, url_for, flash, redirect
from forms import RegisterForm
from main_mod import do_stuff
import secrets
secrets.token_hex(16)

app = Flask(__name__)
app.config["SECRET_KEY"] = '531d9739ed8dab2ebb5d1c38f71c1446'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/check_stock', methods=['GET', 'POST'])
def check_stock():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f"Message sent to {form.phone_no.data} successfully!", "success")
        do_stuff(int(form.threshold.data), form.phone_no.data)
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
