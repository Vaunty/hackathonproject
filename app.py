
from flask import Flask, render_template, request, jsonify
import chat_bot as cb
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = cb.get_response(user_message)
    return jsonify({'response': response})

@app.route('/detect', methods=['POST'])
def detect_objects():
    # Placeholder for object detection logic
    return jsonify({'objects': ['crosswalk', 'bus stop', 'traffic light']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
