
import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.auth import AuthController
from routes.dto.auth import SignupDTO
from .dto import LoginDTO
from secrets import token_hex


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


@router.route('/update', methods=['POST'])
async def update():
    user = session.get('user', {})
    image_path = user['profile_image']

    if str(request.files['profile_image'].mimetype) != 'application/octet-stream':
        image = request.files['profile_image']
        image_type = image.content_type.split('/')[1]
        image_path = f'static/uploads/{token_hex(16)}.{image_type}'
        image.save(image_path)

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    await AuthController.update(
        first_name, last_name, image_path
    )

    return redirect(request.referrer + '#update_modal')


@router.route('/logout')
async def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@router.route('/forgot')
async def forgot():
    return render_template('auth/forgot.html')
