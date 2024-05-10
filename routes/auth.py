
import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash ,session
from controllers.auth import AuthController
from routes.dto.auth import SignupDTO
from .dto import LoginDTO

router = Blueprint('auth', __name__)


@router.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        dto = LoginDTO(**request.form)
        if await AuthController.login(dto):
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        else:
            return render_template('auth/login.html', error='Invalid email or password',)


    return render_template('auth/login.html')


@router.route('/signup', methods=['GET', 'POST'])
async def signup():
    if request.method == 'POST':
        try:
            dto = SignupDTO(**request.form)
            await AuthController.signup(dto)
            flash('Signed up successfully', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            logging.critical(str(e))
            return render_template('auth/signup.html', error=str(e))

    return render_template('auth/signup.html')



@router.route('/logout')
async def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@router.route('/forgot')
async def forgot():
    return render_template('auth/forgot.html')