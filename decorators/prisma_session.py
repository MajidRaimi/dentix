from prisma import Prisma

def prisma_session(func):
    async def wrapper(*args, **kwargs):
        prisma = Prisma()
        await prisma.connect()
        try:
            response = await func(*args, prisma=prisma, **kwargs)
        finally:
            await prisma.disconnect()
        return response
    return wrapper