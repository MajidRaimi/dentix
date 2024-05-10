from functools import wraps
from flask import session, redirect, request, url_for
import json

ROLE_HIERARCHY = ['DOCTOR', 'ADMIN', 'SUPER_ADMIN']

def auth(minimum_role):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('auth.login'))
            user_data = session.get('user', '{}')
            user_role = user_data.get('role')
            referrer = request.referrer
            if user_role is None or ROLE_HIERARCHY.index(user_role) < ROLE_HIERARCHY.index(minimum_role):
                if referrer is None:
                    return redirect(url_for('auth.login'))
                else:
                    return redirect(referrer)
            return await func(*args, **kwargs)
        return wrapper
    return decorator