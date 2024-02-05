from flask import Blueprint, render_template, abort, redirect, url_for, request, session, flash
import os
from datetime import datetime, date
import requests
import core.cryptography as cg
import yaml
import dotenv


view_plan = Blueprint('plan', __name__, template_folder='templates', url_prefix='/vp')


@view_plan.route("/schuelogin")
def schuelogin():
    return render_template("schuelogin.html")

@view_plan.route("/schuelogin", methods=['POST'])
def schuelogin_post():
    flash("Validating...")
    if cg.hash_password(request.form['password']) == yaml.safe_load(open(os.path.join("data", request.form['scident'], f'proto.yml')))['users'][request.form['username']]['password']:
        session['user'] = request.form['username']
        session['password'] = request.form['password']
        session['scident'] = request.form['scident']
        return redirect(url_for('plan.dashboard'))
    abort(401)

@view_plan.route("/lehrerlogin")
def lelogin():
    return render_template("schuelogin.html")

@view_plan.route("/lehrerlogin", methods=['POST'])
def lelogin_post():
    flash("Validating...")
    if cg.hash_password(request.form['password']) == yaml.safe_load(open(os.path.join("data", request.form['scident'], f'proto.yml')))['users'][request.form['username']]['password']:
        session['user'] = request.form['username']
        session['password'] = request.form['password']
        session['scident'] = request.form['scident']
        return redirect(url_for('plan.dashboard'))
    abort(401)

@view_plan.route("/day/<day>")
def dayview(day):
    iso_date = datetime.fromisoformat(day)
    if 'user' in session and 'password' in session and 'scident' in session:
        r = requests.get(f'http://{os.environ["HOST"]}:{os.environ["PORT"]}/api/day/{session["scident"]}/{iso_date.isoformat()}', headers={'X-User': session['user'], 'X-Access-Hash': session['password']})
        data = r.json()
        return render_template("dayview.html", data=data, date=iso_date, classid=request.args.get("cls"))
    else:
        return redirect(url_for("plan.schuelogin"))

@view_plan.route("/dashboard")
def dashboard():
    if 'user' in session:
        if session['user'] == 'admin':
            return render_template("panel.html")
        return render_template("dashboard.html")

@view_plan.route("/plan/edit")
def pedit():
    if 'user' in session:
        if session['user'] == 'admin':
            return render_template("editplan.html")
        abort(401)


@view_plan.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('password', None)
    session.pop('scident', None)
    return redirect(url_for('main'))