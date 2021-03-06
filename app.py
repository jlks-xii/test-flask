from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import firebase_admin
from firebase_admin import credentials, firestore

# Use the application default credentials
# firebase_admin.initialize_app(cred, {
#    'projectId': 'new-db-test'
# })

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)
CORS(app)

Games = [
    {'name': 'Tales of Symphonia'},
    {'name': 'Tales of the Abyss'},
    {'name': 'Tales of Vesperia'}
]


@app.route('/games', methods=['GET'])
def index():
    Users = []
    users_ref = db.collection(u'users')
    docs = users_ref.get()

    for doc in docs:
        user = {
            'id': doc.id,
            'data': doc.to_dict()
        }
        Users.append(user)
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))

    return jsonify(Users)


@app.route('/user/add', methods=['POST'])
def addUser():
    post_data = request.get_json()
    username = post_data.get('username')

    doc_ref = db.collection(u'users').document()
    doc_ref.set({
        u'name': username,
    })

    return jsonify({
        'status': 'ok',
        'message': username + ' added'
    })


@app.route('/game/add', methods=['POST'])
def add():
    post_data = request.get_json()
    game_name = post_data.get('game')
    new_game = {'name': game_name}
    Games.append(new_game)
    return jsonify({'added': game_name + ' added.'})


@app.route('/user/<userid>/delete', methods=['DELETE'])
def deleteUser(userid):
    db.collection(u'users').document(userid).delete()

    return jsonify({
        'status': 'ok',
        'message': 'User deleted.'
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
