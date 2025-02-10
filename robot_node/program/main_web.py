import os
from flask import Flask, render_template, Response, send_from_directory
from robot_node.camera import VideoCamera

app = Flask(__name__)

@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory('image', filename)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/controllor')
def controllor():
    return render_template('controllor.html')

@app.route('/config')
def config():
    return render_template('config.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/test_server')
def test_server():
    return render_template('test_server.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame
            + b'\r\n\r\n')
        
@app.route('/video_cap')
def video_cap():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)