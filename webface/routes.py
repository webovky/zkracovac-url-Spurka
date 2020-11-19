from . import app
from flask import render_template, request, redirect, url_for, session
import functools
from werkzeug.security import generate_password_hash, check_password_hash
from pony.orm import db_session


def login_required(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def index():
    return render_template("base.html.j2")


@app.route("/<string:shortcut>", methods=["GET"])
def short_redirect(shortcut):
    return render_template("base.html.j2")


@app.route("/adduser/", methods=["GET"])
def adduser():
    return render_template("adduser.html.j2")

@app.route("/adduser/", methods=["POST"])

def adduser_post():
    login = request.form.get('login')
    passwd1 = request.form.get('passwd1')
    passwd2 = request.form.get('passwd2')
    user = User[login]
    user = User.get(login=login)
    if user:
        flash("uzivatel jiz existuje")
        print(user.login, user.password)
    if len(passwd1) >= 5 and passwd1 == passwd2:
        user = User(login=login, password=generate_password_hash(passwd1))
        flash("ucet vytvoren")
    else:
        flash('hesla nejsou stejna, nebo jsou prilis kratka')
        return redirect(url_for('adduser'))
    return render_template("index")


@app.route("/login/")
def login():
    return render_template("login.html.j2")


@app.route("/logout/")
def logout():
    return render_template("base.html.j2")
