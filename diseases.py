import json
from this import d

from flask import Blueprint, Flask, jsonify
from flaskext.mysql import MySQL
from config import Config
from flask import request



diseases_bp = Blueprint('diseases', __name__)
app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL()

mysql.init_app(app)



@diseases_bp.route('/', methods=['GET'])
def diseaseTest():
    return (jsonify({
            'success': 'true',
            'message': 'Diseases API Connected',
            'status': 200
        }))



@diseases_bp.route('/<key>', methods=['GET'])
def fetchDisease(key):

    disease = fetchDisease(key)
    if not disease or len(disease) == 0:
        return (jsonify({
            'success': 'false',
            'message': 'Disease not found',
            'status': 200
        }))


    diseaseData = {}
    diseaseData['id'] = disease[0]
    diseaseData['disease'] = disease[1]
    diseaseData['about'] = disease[2]
    diseaseData[ 'cure'] = disease[3]
    diseaseData[ 'created_at'] = disease[4]

    disease_id = disease[0]
    docs = fetchDiseaseDoctors(disease_id)

    doctorsData = []

    if docs and len(docs) > 0 :
        for doc in docs:
            doctorsData.append({
                'id': doc[0],
                'fullname': doc[2],
                'image': doc[3],
                'phone': doc[4],
                'email': doc[5],
                'bio': doc[6],
                'created_at': doc[7],
            })
    
    diseaseData['doctors'] = doctorsData
    return (jsonify({
            'success': 'true',
            'message': 'Disease Fetched completed',
            'data' : diseaseData,
            'status': 200
        }))

def fetchDisease(key):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diseases WHERE id = '" + key + "' OR disease = '" + key + "' ")
    return cursor.fetchone()


def fetchDiseaseDoctors(disease_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors WHERE disease_id = '" + str(disease_id) + "' ")
    return cursor.fetchall()


