from flask import Flask, render_template, request, redirect, url_for, flash, Response
import requests
import hashlib
from ecdsa import SigningKey
import cv2
import pyaudio
import numpy as np
import threading

app = Flask(__name__)
app.secret_key = "secret_key"

VERIFICATION_SERVER = "http://127.0.0.1:5001"  # Verification Server
TALLY_SERVER = "http://127.0.0.1:5002"  # Tally Server


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)
audio_threshold = 0.2
sound_check_passed = False
face_check_passed = False


lock = threading.Lock()

def load_private_key():
    with open("client_private_key.pem", "rb") as key_file:
        return SigningKey.from_pem(key_file.read())

def detect_faces_and_sound():
    global face_check_passed, sound_check_passed
    face_check_passed = False
    sound_check_passed = False


    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    def get_audio_level():
        data = np.frombuffer(stream.read(1024, exception_on_overflow=False), dtype=np.int16)
        return np.sqrt(np.mean(data ** 2)) / 32768

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break


        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

        sound_level = get_audio_level()

        with lock:
            face_check_passed = len(faces) == 1
            sound_check_passed = sound_level < audio_threshold

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.putText(frame, f"Faces detected: {len(faces)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Sound Level: {sound_level:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        if not face_check_passed:
            cv2.putText(frame, "Error: More than one face detected!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        if not sound_check_passed:
            cv2.putText(frame, "Error: Sound level too high!", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        _, encoded_frame = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(detect_faces_and_sound(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_check', methods=['POST'])
def start_check():
    global face_check_passed, sound_check_passed
    import time
    time.sleep(2)

    with lock:
        if not face_check_passed:
            flash("Environment check failed: Ensure exactly one face is detected.")
            return redirect(url_for('index'))
        if not sound_check_passed:
            flash("Environment check failed: Reduce background noise.")
            return redirect(url_for('index'))

    return redirect(url_for('vote_page'))

@app.route('/vote_page')
def vote_page():
    return render_template('vote.html')

@app.route('/vote', methods=['POST'])
def vote():
    voter_id = request.form['voter_id']
    candidate = request.form['candidate']

    private_key = load_private_key()
    hashed_message = hashlib.sha256(voter_id.encode()).digest()
    signature = private_key.sign(hashed_message).hex()
    public_key = private_key.get_verifying_key().to_string().hex()

    verification_data = {
        "voter_id": voter_id,
        "signature": signature,
        "public_key": public_key
    }
    response = requests.post(f"{VERIFICATION_SERVER}/verify", json=verification_data)
    if response.status_code != 200:
        error_message = response.json().get("message", "Verification failed")
        return redirect(url_for('failure', message=error_message))

    tally_data = {"vote": candidate}
    response = requests.post(f"{TALLY_SERVER}/tally", json=tally_data)
    if response.status_code != 200:
        error_message = response.json().get("message", "Tallying failed")
        flash(error_message)
        return redirect(url_for('failure', message=error_message))

    update_data = {"voter_id": voter_id}
    response = requests.post(f"{VERIFICATION_SERVER}/update", json=update_data)
    if response.status_code != 200:
        error_message = response.json().get("message", "Update failed")
        flash(error_message)
        return redirect(url_for('failure', message=error_message))

    # flash("Vote submitted successfully!")
    return redirect(url_for('success'))

@app.route('/failure')
def failure():
    message = request.args.get('message', 'An unknown error occurred')
    return render_template('failure.html', message=message)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
