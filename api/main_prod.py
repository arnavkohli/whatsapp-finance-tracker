from flask import Flask, request, jsonify
import json
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse


from manager import *

from messenger import *

app = Flask(__name__)

config = json.loads(open('/home/akohli/mysite/config.json', 'r').read())
manager = Manager(config)

users = manager.get_users()
transactions = manager.get_transactions()

messenger = Messenger(config)

@app.route('/sms', methods=['POST', 'GET'])
def command():
    resp = MessagingResponse()
    try:
        txn_data = messenger.parse_message(request.form['Body'])
        print (txn_data)
    except Exception as e:
        print (e)
        resp.message(e)

    cmd = txn_data['cmd']
    try:
        data = txn_data['data']
    except:
        data = None

    user = manager.get_user_by_number(request.form['From'].split(':')[-1])
    user_id = user['id']

    if cmd == 'all':
        try:
            # send message
            # messenger.send_message(
            #     to=user['number'],
            #     body=manager.clean_user_transactions(user_id, types='all')
            # )

            #return jsonify({"result" : "success. message sent"})
            resp.message(manager.clean_user_transactions(user_id, types='all'))
        except Exception as e:
            print (e)
            #return jsonify({"error" : f"{e}"}), 400
            resp.message('Could not fetch your transactions.')

    elif cmd == 'add':
        data['user_id'] = user_id
        add_txn(data)
        #return jsonify({"result" : "success"}), 200
        resp.message(f"Added transaction #{data['id']}.")
    elif cmd == 'update':
        data['user_id'] = user_id
        update_txn(data)
        #return jsonify({"result" : "success"}), 200
        resp.message(f"Updated transaction #{data['id']}.")
    elif cmd == 'delete':
        delete_txn(data['id'])
        #return jsonify({"result" : "success"}), 200
        resp.message(f"Deleted transaction #{data['id']}.")
    else:
        resp.message('Invalid command.')

    return str(resp)





@app.route('/user_transaction/<int:eyed>', methods=['GET'])
def user_transactions(eyed):
    types = request.args.get('types')
    try:
        return jsonify(manager.get_user_transactions(eyed, types)), 200
    except Exception as e:
        return jsonify({"error" : f"{e}"}), 400

@app.route('/user/<int:eyed>', methods=['GET'])
def user(eyed):
    try:
        return jsonify(manager.get_user(eyed)), 200
    except:
        return jsonify({"error" : "bad request"}), 400

@app.route('/user', methods=['POST'])
def add_user():
    user  = request.get_json()
    try:
        manager.add_user(user)
        return jsonify({"result" : "success"}), 200
    except Exception as e:
        return jsonify({"error" : f"{e}"}), 400


@app.route('/user', methods=['PUT'])
def update_user():
    updated_user = request.get_json()
    try:
        manager.update_user(updated_user)
        return {"result" : "success"}, 200
    except Exception as e:
        return jsonify({"error" : f"{e}"}), 400


@app.route('/user/<int:eyed>', methods=['DELETE'])
def delete_user(eyed):
    try:
        manager.delete_user(eyed)
        return {"result" : "success"}, 200
    except:
        return jsonify({"error" : "bad request"}), 400


@app.route('/transaction/<int:eyed>', methods=['GET'])
def transaction(eyed):
    try:
        return jsonify(manager.get_transaction(eyed)), 200
    except:
        return jsonify({"error" : "bad request"}), 400

@app.route('/transaction', methods=['POST'])
def add_transaction():
    transaction  = request.get_json()
    try:
        manager.add_transaction(transaction)
        return {"result" : "success"}, 200
    except Exception as e:
        return jsonify({"error" : f"{e}"}), 400

def add_txn(transaction):
    try:
        manager.add_transaction(transaction)
        return {"result" : "success"}, 200
    except Exception as e:
        return jsonify({"error" : f"{e}"}), 400

@app.route('/transaction', methods=['PUT'])
def update_transaction():
    new_transaction = request.get_json()
    try:
        manager.update_transaction(new_transaction)
        return {"result" : "success"}, 200
    except Exception as e:
        return jsonify({"error" : f"{e}"}), 400

def update_txn(new_transaction):
    try:
        manager.update_transaction(new_transaction)
        return {"result" : "success"}, 200
    except Exception as e:
        return jsonify({"error" : f"{e}"}), 400


@app.route('/transaction/<int:eyed>', methods=['DELETE'])
def delete_transaction(eyed):
    try:
        manager.delete_transaction(eyed)
        return {"result" : "success"}, 200
    except:
        return jsonify({"error" : "bad request"}), 400

def delete_txn(eyed):
    try:
        manager.delete_transaction(eyed)
        return {"result" : "success"}, 200
    except:
        return jsonify({"error" : "bad request"}), 400



if __name__ == '__main__':
    app.run(debug=True, port=8080)