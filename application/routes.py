from application import app
from flask import render_template, request, Response, json

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


@app.route('/register')
def register():
    return render_template("register.html", register=True)


@app.route('/login')
def login():
    return render_template("login.html", login=True)


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

