from flask.json import dump
from sqlalchemy import MetaData

from application import app, db
from flask import render_template, request, Response, json, redirect, flash, url_for

from application.forms import LoginForm, RegisterForm
from application.models import Users

test_data = [{"id": "1", "title": "test1"}, {"id": "2", "title": "test2"}]


@app.route('/')
def home():
    return 'Hello World'


@app.route('/index')
@app.route('/home')
def index():
    return render_template("index.html", index=True)


@app.route('/test/')
@app.route('/test/<id>')
def test(id="1"):
    return render_template("test.html", testData=test_data, test=True, id=id)


@app.route('/register', methods=['GET', 'POST'])
def register():
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
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(e_mail=email).first()
        if user and user.get_password(password):
            flash("Successfully logged in", "success")
            return redirect("/index")
        else:
            flash("Login error", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route('/enrollment', methods=["GET", "POST"])
def enrollment():
    id = request.form.get('id')
    title = request.form.get('title')
    return render_template("enrollment.html", enrollment=True, data={"id": id, "title": title})


@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if (idx == None):
        jdata = test_data
    else:
        jdata = test_data[int(idx)]

    return Response(json.dumps(jdata), mimetype="application/json")


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
    print("schema" + str(db.metadata.schema))
    __table_name__ = {'users'}
    __table_args__ = {'schema': 'wn'}
    db.metadata.schema = 'wn'
    print("schema" + str(db.metadata.schema))
    users = Users.query.all()
    return render_template("/user.html", users=users)

