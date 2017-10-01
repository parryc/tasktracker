#!/usr/bin/env python
# coding: utf-8
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, login_required,\
                        logout_user, current_user, AnonymousUserMixin
from flask_permissions.core import Permissions
from datetime import datetime
from werkzeug.contrib.cache import MemcachedCache
import os

app           = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db            = SQLAlchemy(app)
assets        = Environment(app)
csrf          = CSRFProtect()
login_manager = LoginManager()
perms         = Permissions(app, db, current_user)

login_manager.init_app(app)
#add csrf protection across the board
csrf.init_app(app)

# Blueprints
from app.mod_tasks.controllers import mod_tasks
from app.mod_projects.controllers import mod_projects
from app.mod_users.controllers import mod_users

# Register blueprints
app.register_blueprint(mod_tasks)
app.register_blueprint(mod_projects)
app.register_blueprint(mod_users)

@app.route('/')
@login_required
def index():
  return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404


@login_manager.user_loader
def load_user(userid):
  return get_user(userid)

class PermissableAnonymousUserMixin(AnonymousUserMixin):
  roles = ['user']
  def __init__(self,roles=roles):
    self.roles = roles
    AnonymousUserMixin.__init__(self)

login_manager.anonymous_user         = PermissableAnonymousUserMixin
login_manager.login_view             = "login"
login_manager.login_message_category = "error"

from app.mod_users.forms import *
from app.mod_users.models import *
@app.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    # login and validate the user...
    user = get_user_by_email(form.email.data)
    if user is not None and user.validate_password(form.password.data):
      if login_user(user):
        user.last_logged_in = datetime.utcnow()
        user.logged_in = True
        db.session.commit()
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
      else:
        flash("Your username or password was invalid.","error")
        return redirect(url_for("login"))
    else:
      if user.external:
        flash("Cannot log in with external account.", "error")
      else:
        flash("Wrong username or password.", "error")
      return redirect(url_for("login"))
  return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
  current_user.logged_in = False
  db.session.commit()
  logout_user()
  return redirect(url_for("login"))