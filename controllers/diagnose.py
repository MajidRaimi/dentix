
import os
from prisma import Prisma
from decorators import prisma_session
from helpers.predict_helper import PredictHelper
import logging
from flask import session
from prisma.models import Label

helper = PredictHelper(os.getcwd() + '/static/models/best_08.pt')



class DiagnoseController():

    @staticmethod
    @prisma_session
    async def diagnose(title: str, image_path:str,prisma:Prisma):
        results = helper.predict(image_path)
        labeled_path = helper.draw_prediction(image_path, results)
        labels = [{'label': label, 'score': score} for label, score, _ in results]

        user_id = session.get('user')['id']

        prediction = await prisma.prediction.create(
            data={
                'title': title,
                'image': image_path,
                'result': labeled_path,
                'user_id': user_id,
                'labels': {
                    'create': labels
                }
            }
        )

        return prediction.id

    @staticmethod
    @prisma_session
    async def get_diagnoses(prisma:Prisma):
        user_id = session.get('user')['id']
        diagnoses = await prisma.prediction.find_many(
            where={
                'user_id': user_id
            }
        )

        logging.critical(diagnoses)


        diagnoses = [diagnose.model_dump() for diagnose in diagnoses]

        return diagnoses

    @staticmethod
    @prisma_session
    async def get_diagnose(prediction_id:str, prisma:Prisma):
        prediction = await prisma.prediction.find_unique(
            where={
                'id': prediction_id
            }
        )

        labels = await prisma.label.find_many(
            where={
                'predictionId': prediction.id
            }
        )

        prediction = dict(prediction)
        labels = [label.model_dump() for label in labels]

        return prediction, labels