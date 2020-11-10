from app import cat
from flask import render_template


@cat.route("/")
@cat.route("/index")
def hello():
    user = {"username": "Rishabh"}
    posts = [
        {
            "author": {"username": "Shekhar"},
            "post":  "what an exciting future"
        },
        {
            "author": {"username": "Ankur"},
            "post": "Long fight ahead"
        },
    ]
    return render_template("index.html", title="Den", user1=user, post1=posts)
