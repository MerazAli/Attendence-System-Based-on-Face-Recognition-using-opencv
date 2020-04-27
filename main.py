from flask import Flask,render_template,request,Response
from videostream import VideoCamera
app=Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')



    # code for  camera in flask

@app.route('/gen')
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')    


#@app.route('/open_camera')  
#def open_camera():


#@app.route('/enroll') 
#def enroll():



if __name__=='__main__':
    app.run(debug=True)
