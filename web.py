from flask import Flask, Response, jsonify
import cv2
import numpy as np
import main as main

app = Flask(__name__)

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)
current_coordinates = {"x": None, "y": None}

def generate_frames():
    global current_coordinates
    while True:
        main

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/coordinates')
def get_coordinates():
    return jsonify(current_coordinates)

@app.route('/')
def index():
    return '''
    <html>
        <head>
            <title>Video Stream with Coordinates</title>
            <script>
                function fetchCoordinates() {
                    fetch('/coordinates')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('coordinates').innerText = 'X: ' + data.x + ' Y: ' + data.y;
                        })
                        .catch(error => console.error('Error fetching coordinates:', error));
                }
                setInterval(fetchCoordinates, 500); // Update every 500ms
            </script>
        </head>
        <body>
            <h1>Video Stream with Coordinates</h1>
            <div>
                <img src="/video_feed" width="720" height="480" />
            </div>
            <div>
                <h2>Coordinates:</h2>
                <p id="coordinates">X: None, Y: None</p>
            </div>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
