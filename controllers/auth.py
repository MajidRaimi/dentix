from flask import session
from prisma import Prisma

from decorators import prisma_session
from lib import send_welcome_email
from routes.dto.auth import LoginDTO, SignupDTO
from bcrypt import hashpw, gensalt, checkpw

class AuthController:

    @staticmethod
    @prisma_session
    async def login(dto: LoginDTO, prisma:Prisma):
        user = await prisma.user.find_unique(where={'email': dto.email})
        if not user:
            return False
        if not checkpw(dto.password.encode(), user.hashed_password.encode()):
            return False
        user = user.model_dump()
        if user['hashed_password']:
            del user['hashed_password']

        if user:
            session['user'] = user
            return True
        return False

    @staticmethod
    @prisma_session
    async def signup(dto:SignupDTO, prisma:Prisma):
        if await prisma.user.find_unique(where={'email': dto.email}):
            raise Exception('Email already exists')

        salt = gensalt()
        hashed_password = hashpw(dto.password.encode(), salt)

        user = await prisma.user.create(data={
            'first_name': dto.first_name,
            'last_name': dto.last_name,
            'email': dto.email,
            'phone_number': dto.phone_number,
            'hashed_password': str(hashed_password, 'utf-8'),
            'role': 'DOCTOR',
            'profile_image': f'https://boring-avatars-api.vercel.app/api/avatar?size=40&variant=beam&name={dto.phone_number}'
        })

        user = await prisma.user.find_unique(where={'id': user.id})

        user = user.model_dump()
        if user['hashed_password']:
            del user['hashed_password']
        if user:
            session['user'] = user
            send_welcome_email(user['email'], user['first_name'])
            return True
        return False

    @staticmethod
    async def logout():
        try:
            session.pop('user', None)
            return True
        except:
            return False