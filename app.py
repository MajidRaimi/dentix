from flask import Flask, request, render_template, session, flash, redirect, url_for
from lib import send_welcome_email
from routes import auth_router, diagnose_router, dashboard_router
from dotenv import load_dotenv
import os
import json
import coloredlogs, logging
from middleware import auth

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(auth_router)
app.register_blueprint(diagnose_router, url_prefix='/diagnose')
app.register_blueprint(dashboard_router, url_prefix='/dashboard')

@app.route('/')
async def index():
    return render_template('index.html', user=session.get('user', {}))

@app.errorhandler(404)
async def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    coloredlogs.install()
    load_dotenv()
    app.run(debug=True if os.getenv('PYTHON_ENV') == 'development' else False, port=os.getenv('PORT'))
