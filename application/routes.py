from flask.json import dump
from sqlalchemy import MetaData

from application import app, db
from flask import render_template, request, Response, json, redirect, flash, url_for, session
from application.forms import LoginForm, RegisterForm
from application.models import Users


@app.route('/')
def home():
    return 'Hello World'


@app.route('/index')
@app.route('/home')
def index():
    return render_template("index.html", index=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = Users.query.count()
        user_id += 1

        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        new_user = Users(id=user_id, e_mail=email, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Successfully registered in", "success")
        return redirect(url_for('index'))

    return render_template("register.html", title="Register", form=form, register=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(e_mail=email).first()
        if user and user.get_password(password):

            user_agent = request.headers.get('User-Agent')
            user_agent = user_agent.lower()

            flash(f"Successfully logged in {user_agent}", "success")
            session['user_id'] = user.id
            session['username'] = user.first_name
            return redirect("/index")
        else:
            flash("Login error", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route('/logout')
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/users", methods=['GET'])
def user():
    form = LoginForm()
    try:
        new_user = Users(id=3, first_name="asia", last_name="last_test", e_mail="test@test.pl", password="test")
        db.session.add(new_user)
        db.session.commit()
        flash("user created", "success")
        return redirect("/index")
    except:
        flash("user not saved", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route('/user')
def get_users():
    if not session.get('username'):
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    print(user_id)
    users = Users.query.all()
    return render_template("user.html", users=users)


@app.route('/devices/', methods=['GET', 'POST'])
def get_devices():
    if not session.get('username'):
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    print(user_id)
    users = Users.query.all()
    return render_template("devices.html", title="Login", users=users, devices=True)
