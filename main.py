from flask import Flask, render_template, redirect, url_for, request, session, flash, abort
import os
from blueprints import api, frontend
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

app.register_blueprint(api.planapi)
app.register_blueprint(frontend.view_plan)

@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for("plan.schuelogin"))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=int(os.environ['DEBUG']), host=os.environ['HOST'], port=int(os.environ['PORT']))