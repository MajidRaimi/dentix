import logging
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from secrets import token_hex
from config.allowed_files import ALLOWED_FILES
from controllers.diagnose import DiagnoseController
from middleware import auth


controller = DiagnoseController()

router = Blueprint('/diagnose', __name__)

@router.route('/', methods=['POST'])
@auth('DOCTOR')
async def diagnose():
    file = request.files['file']
    title = request.form['title']
    # patient = request.form['patient']
    file_extension = file.filename.split('.')[-1]
    if file_extension not in ALLOWED_FILES:
        flash('Invalid file type', 'error')
        return redirect(request.referrer)
    file.filename = token_hex(16) + '.' + file_extension
    file_path = f'static/uploads/{file.filename}'
    file.save(file_path)

    prediction_id = await controller.diagnose(title, file_path)
    return redirect(f'/diagnose/{prediction_id}')

@router.route('/all', methods=['GET'])
@auth('DOCTOR')
async def diagnoses():
    diagnoses = await controller.get_diagnoses()
    return render_template('diagnose/all.html', diagnoses=diagnoses, user=session.get('user', {}))



@router.route('/<string:id>', methods=['GET', 'POST'])
@auth('DOCTOR')
async def diagnose_id(id):
    prediction, labels = await controller.get_diagnose(id)

    for index, label in enumerate(labels):
        labels[index]['score'] = round(label['score'] * 100, 2)
        labels[index]['index'] = index



    return render_template('diagnose/diagnose.html', prediction=prediction, labels=labels, user=session.get('user', {}))

