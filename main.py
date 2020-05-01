from flask import Flask,render_template,request,Response
from videostream import VideoCamera
from face_enroll import register_cam
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gen')
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/camera')
def video_feed():
    print(type(gen(VideoCamera())))
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')    


@app.route('/register') 
def enroll():
    register_cam()
    return render_template('face_register.html',)



if __name__=='__main__':
    app.run(debug=True)
