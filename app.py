# -*- coding: utf-8 -*-

# Required Imports
import os
from time import sleep
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import webscrap

# Initialize Flask App
app = Flask(__name__)
# Initialize Firestore DB
cred = credentials.Certificate('upidata-f23a4-firebase-adminsdk-fxqed-e1e9866762.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('applications')
@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')    
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            print(all_todos)
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"
@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
    
    
def update_db():
    df = webscrap.get_data()

    data_dict = df.to_dict("records")
    for i in range(len(data_dict)):
        data_dict[i]['id'] = str(i)
        data_dict[i] = webscrap.correct_encoding(data_dict[i])

    api_endpoint = "http://127.0.0.1:5000"

    delete()
    create(data_dict, api_endpoint)


if __name__ == "__main__":

    while True:

        update_db()

        sleep(86400)