from flask import Blueprint, render_template, abort, redirect, url_for, request, session, jsonify
import os
from datetime import datetime, date
import yaml
from core import cryptography as cg

planapi = Blueprint('planapi', __name__, template_folder='templates', url_prefix='/api')

@planapi.route("/day/<scident>/<day>")
def get_day(scident,day):
    iso_date = datetime.fromisoformat(day)
    user = request.headers.get('X-User')
    password = request.headers.get('X-Access-Hash')
    # Rest of your code here
    if os.path.exists(os.path.join("data", scident, f'proto.yml')):
        proto = yaml.safe_load(open(os.path.join("data", scident, f'proto.yml')))
        if cg.hash_password(password) == proto['users'][user]['password']:
            if os.path.exists(os.path.join("data", scident, f'{iso_date:%Y-%m-%d}.yaml')):
                with open(os.path.join("data", scident, f'{iso_date:%Y-%m-%d}.yaml')) as f:
                    return jsonify(yaml.load(f, Loader=yaml.FullLoader))
            elif os.path.exists(os.path.join("data", scident, 'default.yaml')):
                with open(os.path.join("data", scident, 'default.yaml')) as f:
                    return jsonify(yaml.load(f, Loader=yaml.FullLoader))
            
            abort(404)
        abort(401)
    abort(404)

@planapi.route("/p-add", methods=['POST'])
def plan_add():
    if 'user' in session and session.get('user') == 'admin':
        if os.path.exists(os.path.join('data', session['scident'], f'{date.today().isoformat()}.yaml')):
            data = yaml.safe_load(open(os.path.join('data', session['scident'], f'{date.today().isoformat()}.yaml')))
        else:
            data = {
                'metadata': {
                    'school': session['scident'],
                    'date': date.today().isoformat(),
                    'name': date.today().isoformat(),
                },
                'classes': {}
            }
        d = request.form.to_dict()
        cname = d.pop('klasse')
        cls = [{} for i in range(7)]
        data['metadata']['date'] = data['metadata']['name'] = d.pop('date-for')
        for key, value in d.items():
            index = int(key[0])
            name = key[1:]
            cls[index]['lesson'] = index+1
            if name == "Fa":
                cls[index]['subject'] = value
            elif name == "Ra":
                cls[index]['room'] = value
            elif name == "Zi":
                cls[index]['info'] = value
            elif name == "Le":
                cls[index]['teacher'] = value
        data['classes'][cname] = cls
        yaml.safe_dump(data, open(os.path.join('data', session['scident'], f'{date.today().isoformat()}.yaml'), 'w+'))
        return redirect(url_for('plan.dashboard'))
    abort(401)

@planapi.route("/day/<scident>/<day>", methods=['POST'])
def post_day(scident,day):
    iso_date = datetime.fromisoformat(day)
    user = request.headers.get('X-User')
    password = request.headers.get('X-Access-Hash')
    # Rest of your code here
    if os.path.exists(os.path.join("data", scident, f'proto.yml')):
        proto = yaml.safe_load(open(os.path.join("data", scident, f'proto.yml')))
        if password == proto['users'][user]['password'] and user == "admin":
            request.files['file'].save(os.path.join("data", scident, f'{iso_date:%Y-%m-%d}.yaml'))
            return jsonify(yaml.load(open(os.path.join("data", scident, f'{iso_date:%Y-%m-%d}.yaml')), Loader=yaml.FullLoader))

        abort(401)
    abort(404)