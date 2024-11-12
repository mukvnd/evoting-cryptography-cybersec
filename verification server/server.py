from ecdsa import VerifyingKey, BadSignatureError
import hashlib
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

VOTERS_FILE = "voter_data.json"


def load_voters():
    with open('voter_data.json', "r") as file:
        data = json.load(file)
        return data


def save_voters(voters_data):
    with open("voter_data.json", "w") as file:
        json.dump(voters_data, file, indent=4)

@app.route('/verify', methods=['POST'])
def verify_voter():
    voters_data = load_voters()

    data = request.json
    voter_id = data.get("voter_id")
    signature = data.get("signature")
    public_key_hex = 'client_public_key.pem'

    found = False
    for voter in voters_data['voters']:
        if voter['id'] == voter_id:
            print(voter['id'])
            found = True
            if voter["voted"]:
                return jsonify({"status": "error", "message": "Voter has already voted"}), 403
    print(found)
    if not found:
        return jsonify({"status": "error", "message": "Voter not found"}), 400
    
    try:
        with open("client_public_key.pem", "rb") as key_file:
            server_public_key = VerifyingKey.from_pem(key_file.read())
        hashed_message = hashlib.sha256(voter_id.encode()).digest()
        server_public_key.verify(bytes.fromhex(signature), hashed_message)
    except BadSignatureError:
        return jsonify({"status": "error", "message": "Invalid signature"}), 401

    return jsonify({"status": "success", "message": "Voter verified"}), 200

@app.route('/update', methods=['POST'])
def update_voter_status():
    voters_data = load_voters()

    data = request.json

    print(data)
    voter_id = data.get("voter_id")

    for voter in voters_data['voters']:
        if voter['id'] == voter_id:
            voter['voted'] = True
    save_voters(voters_data)

    return jsonify({"status": "success", "message": "Voter status updated"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
