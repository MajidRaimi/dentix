
from flask import Blueprint, render_template, session, request, redirect, url_for, flash

from controllers.dashboard import DashboardController

router = Blueprint('dashboard', __name__)

@router.route('/')
def index():
    return render_template('dashboard/index.html', user=session.get('user', {}))

@router.route('/users')
async def users():
    users = await DashboardController.get_users()
    return render_template('dashboard/users.html', user=session.get('user', {}), users=users)

@router.route('/users/inspect/<string:id>', methods=['GET'])
async def inspect_user(id):
    diagnoses = await DashboardController.get_diagnoses(id)
    return render_template('diagnose/all.html', diagnoses=diagnoses, user=session.get('user', {}))


@router.route('/users/upgrade/<string:id>', methods=['GET'])
async def upgrade_user(id):
    result = await DashboardController.upgrade_user(id)
    return redirect(url_for('dashboard.users'))

@router.route('/users/delete/<string:id>', methods=['GET'])
async def delete_user(id):
    await DashboardController.delete_user(id)
    return redirect(url_for('dashboard.users'))


@router.route('/admins')
async def admins():
    users = await DashboardController.get_admins()
    return render_template('dashboard/admins.html', user=session.get('user', {}), admins=users)


@router.route('/admins/inspect/<string:id>', methods=['GET'])
async def inspect_admin(id):
    diagnoses = await DashboardController.get_diagnoses(id)
    return render_template('diagnose/all.html', diagnoses=diagnoses, user=session.get('user', {}))

@router.route('/admins/downgrade/<string:id>', methods=['GET'])
async def downgrade_admin(id):
    result = await DashboardController.downgrade_admin(id)
    return redirect(url_for('dashboard.admins'))