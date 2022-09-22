from flask import Flask ,render_template,redirect,Blueprint

core=Blueprint("core",__name__)

@core.route("/")
def home():
    return render_template("index.html")


@core.route("/contact")
def contact():
    return render_template("contact.html")

@core.route("/about")
def about():
    return render_template("about.html")