

from prisma import Prisma
from decorators import prisma_session
from prisma.enums import Role
import pymongo
import os


class DashboardController():

    @staticmethod
    @prisma_session
    async def get_users(prisma: Prisma):
        users = await prisma.user.find_many()
        users = [
            user.model_dump() for user in users if user.role != 'ADMIN' and user.role != 'SUPER_ADMIN'
        ]
        return users

    @staticmethod
    @prisma_session
    async def get_diagnoses(user_id: str, prisma: Prisma):
        diagnoses = await prisma.prediction.find_many(
            where={
                'user_id': user_id
            }
        )

        diagnoses = [diagnose.model_dump() for diagnose in diagnoses]

        for diagnose in diagnoses:
            diagnose['created_at'] = diagnose['created_at'].strftime(
                "%d %b %Y %H:%M:%S")

        return diagnoses

    @staticmethod
    @prisma_session
    async def upgrade_user(user_id: str, prisma: Prisma):
        user = await prisma.user.find_unique(
            where={
                'id': user_id
            }
        )

        await prisma.user.delete(
            where={
                'id': user_id
            }
        )

        await prisma.user.create(
            data={
                'id': user.id,
                'email': user.email,
                'hashed_password': user.hashed_password,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': Role.ADMIN,
                'phone_number': user.phone_number,
                'profile_image': user.profile_image,
            }
        )

        try:
            pass
        except Exception as e:
            print(e)
            return False

        return True

    @staticmethod
    @prisma_session
    async def delete_user(user_id: str, prisma: Prisma):
        try:
            await prisma.user.delete(
                where={
                    'id': user_id
                }
            )
        except Exception as e:
            print(e)
            return False

        return True

    @staticmethod
    @prisma_session
    async def get_admins(prisma: Prisma):
        users = await prisma.user.find_many(
            where={
                'role': Role.ADMIN
            }
        )
        users = [
            user.model_dump() for user in users if user.role != 'DOCTOR' and user.role != 'SUPER_ADMIN'
        ]
        return users


    @staticmethod
    @prisma_session
    async def downgrade_admin(user_id: str, prisma: Prisma):
        user = await prisma.user.find_unique(
            where={
                'id': user_id
            }
        )

        await prisma.user.delete(
            where={
                'id': user_id
            }
        )

        await prisma.user.create(
            data={
                'id': user.id,
                'email': user.email,
                'hashed_password': user.hashed_password,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': Role.DOCTOR,
                'phone_number': user.phone_number,
                'profile_image': user.profile_image,
            }
        )