from flask import Blueprint, render_template, abort, redirect, url_for, request, session, jsonify
import os
from datetime import datetime
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