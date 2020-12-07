from app import cat  # import cat object from app(__init__.py)
from flask import render_template, flash, redirect, url_for, request
from app.forms import (
    LoginForm,
    RegistrationForm,
    EditProfileForm,
    EmptyForm,
)  # importing the login, registration form created in forms to access the details
from app.models import (
    User,
)  # importing the user class from models(schema created to save data in it
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)  # handle login authorizations and flow
from werkzeug.urls import url_parse
from app import db
from datetime import datetime


@cat.route("/")
@cat.route("/index")
@login_required  # decorator defining the hello(index) function only be called if user is logged in
def hello():
    user = {"username": "Rishabh"}
    posts = [
        {"author": {"username": "Shekhar"}, "post": "what an exciting future"},
        {"author": {"username": "Ankur"}, "post": "Long fight ahead"},
    ]
    return render_template("index.html", title="Den", user1=user, post1=posts)


@cat.route("/login", methods=["GET", "POST"])
def login():  # really important login function handling flow of log in
    if (
        current_user.is_authenticated
    ):  # primary check to see if current user is authenticated or logged in
        return redirect(url_for("hello"))  # if yes then '/login' redirects to '/index'
    form = (
        LoginForm()
    )  # if not authenticated, login details are asked as per the loginForm created
    if (
        form.validate_on_submit()
    ):  # login details are validated, if validate_on_submit found True condition followed
        user = User.query.filter_by(
            username=form.username1.data
        ).first()  # user = username or None based on query
        if user is None or not user.check_password(
            form.password1.data
        ):  # if user not present or check password fail
            flash(
                " Invalid password or username"
            )  # flash message for above either condition to be ture
        login_user(
            user, remember=form.remember_me1.data
        )  # if user details correct then login_ser makes current_user
        next_page = request.args.get(
            "next"
        )  # ex. /login?next=/index, when redirected to login, then taken back to initial page
        if (
            not next_page or url_parse(next_page).netloc != ""
        ):  # check partial or full url in next
            next_page = url_for(
                "hello"
            )  # next_page variable has stored url for "hello(index)" function
        return redirect(next_page)  # redirected to next_page
    return render_template("login.html", title="Sign In", form1=form)


@cat.route("/logout")  # logout url
def logout():  # function called at url
    logout_user()  # import from flask_login ,takes care of logout, removing current_user session
    return redirect(url_for("hello"))  # redirected to hello(index) url


@cat.route("/register", methods=["GET", "POST"])
def register():
    if (
        current_user.is_authenticated
    ):  # import from flask_login taking care of current user authentication
        return redirect(url_for("index"))
    form = RegistrationForm()
    if (
        form.validate_on_submit()
    ):  # validate on submit() is a method of class Flask_form, is true if all form validators are true
        user = User(
            username=form.username.data, email=form.email.data
        )  # getting data from form User
        user.set_password(
            form.password.data
        )  # setting password hash from password data from form
        db.session.add(user)  # adding user to the session in db instance of SQLAlchemy
        db.session.commit()  # committing to db database
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@cat.route("/user/<username>")
@login_required
def istemal_krta(username):
    user_krta = User.query.filter_by(username=username).first_or_404()
    posts_krta = [
        {"author": user_krta, "body": "Test post #1"},
        {"author": user_krta, "body": "Test post #2"},
    ]
    form = EmptyForm()
    return render_template("user.html", user_krta1=user_krta, posts_krta1=posts_krta, form=form)


@cat.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@cat.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)


@cat.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('hello'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('istemal_krta', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('istemal_krta', username=username))
    else:
        return redirect(url_for('hello'))


@cat.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('hello'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('istemal_krta', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('istemal_krta', username=username))
    else:
        return redirect(url_for('hello'))
