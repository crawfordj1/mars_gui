from flask import *
from camera import VideoCamera

var = False

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    print(var)

@app.route('/goals/')
def goals():
    return render_template('goals.html')

@app.route('/optical/')
def optical():
    return render_template('optical.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen_opti(camera):
    while True:
        frame = camera.opti_dense()
        yield (b'--frame\r\n'
               b'Content-Type:  mage/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed/')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_optical/')
def video_feed_optical():
    return Response(gen_opti(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
