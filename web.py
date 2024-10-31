from flask import Flask, Response, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)
current_coordinates = {"x": None, "y": None}

def generate_frames():
    global current_coordinates
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 45, 45])
        upper_blue = np.array([120, 250, 250])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 10000:  # Filter out small areas
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                current_coordinates = {"x": x, "y": y}
                break  # Use the first large contour found

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame as part of an MJPEG stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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
