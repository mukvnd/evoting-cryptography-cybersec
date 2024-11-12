from flask import Flask, request, jsonify
import json

app = Flask(__name__)

PARTIES = ['BJP', 'Congress', 'AAP', 'NOTA']

def load_tally():
    with open("tally.json", "r") as file:
        return json.load(file)

# saving and updating tally.json to tally the votes
    
def save_tally(tally_data):
    with open("tally.json", "w") as file:
        json.dump(tally_data, file, indent=4)

@app.route('/tally', methods=['POST'])
def update_tally():
    tally_data = load_tally()

    data = request.json
    vote = data.get("vote")
    vote = PARTIES[int(vote)]


    if str(vote) not in tally_data:
        return jsonify({"status": "error", "message": "Invalid vote"}), 402

    tally_data[str(vote)] += 1
    save_tally(tally_data)

    return jsonify({"status": "success", "message": "Vote recorded"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)
