from flask.json import dump
from sqlalchemy import MetaData
import json, time
from application import app, db
from flask import render_template, request, Response, json, redirect, flash, url_for, session
from application.forms import LoginForm, RegisterForm, AddDevice
from application.models import Users, Devices
import cv2

@app.route('/')
def home():
    return 'Hello World'


@app.route('/index')
@app.route('/home')
def index():
    login_state = False
    if session.get('username'):
        login_state = True

    return render_template("index.html", index=True, login=login_state)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        new_user = Users(e_mail=email, first_name=first_name, last_name=last_name)
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

            if "iphone" in user_agent:
                session['device'] = "ios"
            elif "android" in user_agent:
                session['device'] = "android"
            else:
                session['device'] = "web"

            print(session['device'])

            flash(f"Successfully logged in, {user.first_name} ", "success")
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


@app.route("/add_device", methods=['GET', 'POST'])
def add_device():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    form = AddDevice(user_id=user_id)

    if form.validate_on_submit():
        device_name = form.device_name.data
        device_platform = form.device_platform.data

        new_device = Devices(device_name=device_name, device_platform=device_platform, user_id=user_id)
        db.session.add(new_device)
        db.session.commit()

        flash("Successfully added device", "success")
        return redirect(url_for('get_devices'))

    return render_template("add_device.html", title="Add Device", form=form)



@app.route('/user')
def get_users():
    if not session.get('username'):
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    print(user_id)
    users = Users.query.all()
    return render_template("user.html", users=users)


@app.route('/devices/')
def get_devices():
    if not session.get('username'):
        return redirect(url_for('login'))

    devicesList = Devices.query.order_by(Devices.device_id).all()
    return render_template("devices.html", title="Devices", data=devicesList, devices=True)


@app.route('/delete_devices', methods=['GET', 'POST'])
def delete_device():
    form = AddDevice()
    if form.submit():
        data = request.form
        device_id = data['device_id']

        device = Devices.query.filter_by(device_id=device_id).first()
        if device:
            try:
                db.session.delete(device)
                db.session.commit()
                flash("Device successfully deleted", "success")
            except:
                flash("Device not deleted", "danger")

    return redirect(url_for('get_devices'))

@app.route('/devices/stream/<platform>', methods=['GET', 'POST'])
def devices_stream(platform):
    print(platform)
    if not session.get('username'):
        return redirect(url_for('login'))

    return render_template('/stream.html', platform=platform)

@app.route('/devices/watch/<platform>', methods=['GET', 'POST'])
def devices_watch(platform):
    print(platform)
    if not session.get('username'):
        return redirect(url_for('login'))

    return render_template('/watch.html', platform=platform)

def gen_frames():
    camera = cv2.VideoCapture(0)
    camera.grab()
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/camera')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')