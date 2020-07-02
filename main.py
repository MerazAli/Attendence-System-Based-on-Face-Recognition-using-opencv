from flask import Flask,render_template,request,Response,flash,session,redirect
from videostream import VideoCamera
from face_enroll2 import register_cam
from helper import create_user_folder

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column,String,Integer,Float
import pandas as pd
# from database import Products

# connect to database
engine = create_engine('sqlite:///attendance_db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()
# data base code ends

app=Flask(__name__)
app.secret_key= "go revise the concepts"

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


@app.route('/register', methods=["POST","GET"]) 
def enroll():
    if request.method=="POST":
        fullname = request.form.get('fullname')
        rollno = request.form.get('rollno')
        if fullname and rollno:
            if False: # check database
                pass
            else:
                # add the data to databasse
                folder = create_user_folder(fullname,rollno)
                if folder:
                    session['folder'] = folder
                    session['name'] = fullname
                    # to do add to database
                    flash("data created for the user",'success')
                    return redirect('/save_images')
                else:
                    flash('folder not created', 'danger')
        else:
            flash('fill the data', 'warning')
    return render_template('signup.html')

@app.route('/save_images')
def save_images_for_new_user():
    if 'folder' in session:
        folder = session['folder']
        name = session['name']
        register_cam(folder, name)
    else:
        flash('register your id and name first', 'warning')
        return redirect('/register')
    return render_template('face_register.html',)


@app.route('/login_cam')
def login_cam():
    return render_template('result.html')

@app.route('/login')
def login():
    return render_template('login.html')



if __name__=='__main__':
    app.run(debug=True, threaded=True)
