from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def pre_login():
    return render_template("Pré-login.html")


@main.route("/home/")
def home():
    return render_template("index.html")