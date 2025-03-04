from flask import Flask, Response, jsonify, request
import cv2
import numpy as np
import main as main

app = Flask(__name__)

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)
current_coordinates = {"x": None, "y": None}

# Initialize HSV ranges via our added variables. Blue will be our default color
lower_hsv = np.array([100, 45, 45])
upper_hsv = np.array([120, 250, 250])

def generate_frames():
    global current_coordinates, lower_hsv, upper_hsv
    while True:

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/coordinates')
def get_coordinates():
    return jsonify(current_coordinates)

@app.route('/set_hsv', methods=['POST'])
def set_hsv():

    #updates hsv values

    global lower_hsv, upper_hsv
    data = request.json
    lower_hsv = np.array([data['low_h'], data['low_s'], data['low_v']])
    upper_hsv = np.array([data['high_h'], data['high_s'], data['high_v']])
    return jsonify({"message": "HSV updated", "lower_hsv": lower_hsv.tolist(), "upper_hsv": upper_hsv.tolist()})

@app.route('/')
def index():
    return '''
    <html>
        <head>
            <title>Video Stream with Coordinates</title>
            <script>
                function updateHSV() {

                    // Fetch the current HSV values from the sliders

                    const low_h = document.getElementById('low_h').value;
                    const low_s = document.getElementById('low_s').value;
                    const low_v = document.getElementById('low_v').value;
                    const high_h = document.getElementById('high_h').value;
                    const high_s = document.getElementById('high_s').value;
                    const high_v = document.getElementById('high_v').value;

                    document.getElementById('low_h_val').innerText = low_h;
                    document.getElementById('low_s_val').innerText = low_s;
                    document.getElementById('low_v_val').innerText = low_v;
                    document.getElementById('high_h_val').innerText = high_h;
                    document.getElementById('high_s_val').innerText = high_s;
                    document.getElementById('high_v_val').innerText = high_v;

                    fetch('/set_hsv', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            low_h: parseInt(low_h),
                            low_s: parseInt(low_s),
                            low_v: parseInt(low_v),
                            high_h: parseInt(high_h),
                            high_s: parseInt(high_s),
                            high_v: parseInt(high_v)
                        })
                    }).then(response => response.json())
                      .then(data => console.log('HSV Updated:', data));
                }

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
                <h2>HSV Range</h2>
                <label>Low H: <input type="range" id="low_h" min="0" max="179" value="100" oninput="updateHSV()"> <span id="low_h_val">100</span></label><br>
                <label>Low S: <input type="range" id="low_s" min="0" max="255" value="45" oninput="updateHSV()"> <span id="low_s_val">45</span></label><br>
                <label>Low V: <input type="range" id="low_v" min="0" max="255" value="45" oninput="updateHSV()"> <span id="low_v_val">45</span></label><br>
                <label>High H: <input type="range" id="high_h" min="0" max="179" value="120" oninput="updateHSV()"> <span id="high_h_val">120</span></label><br>
                <label>High S: <input type="range" id="high_s" min="0" max="255" value="250" oninput="updateHSV()"> <span id="high_s_val">250</span></label><br>
                <label>High V: <input type="range" id="high_v" min="0" max="255" value="250" oninput="updateHSV()"> <span id="high_v_val">250</span></label>
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
