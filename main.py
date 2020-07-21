from flask import Flask,render_template,request,Response,flash,session,redirect
from videostream import VideoCamera
from face_enroll2 import register_cam
from helper import create_user_folder

import os
import pickle
import pandas as pd
import face_ai as ai
import login_cam as lc
from datetime import date
from sqlalchemy.orm import sessionmaker
from database_orm import Attendance,User
from sqlalchemy import create_engine, Column,String,Integer,Float

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
        college = request.form.get('college')
        year = request.form.get('year')
        course = request.form.get('course')
        if fullname and rollno and year:
                # add the data to database
                user = User(name=fullname,college=college,roll=rollno,year=year,course=course)
                sess.add(user)
                sess.commit()
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
    status= lc.webcam(sess)
    return render_template('result.html',status=status)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/train')
def trainer():
    subjects = ai.get_names()
    print("Preparing data...")
    faces, labels = ai.prepare_training_data()
    print("Data prepared")
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))
    face_recognizer = ai.train_face_ai(faces, labels)
    
    if not os.path.exists('models'):
        os.mkdir('models')
    face_recognizer.write('models/ai.xml')
    print("model saved")
    return redirect('/')


#@app.route('/view')
#def attendance_view():
#    data = pd.read_sql('attendance',engine)
#   return render_template('attendance.html',data = data.to_html(classes=('table','table-hovered','table-sm','table-responsive'),max_rows=None,max_cols=None,table_id='attendance',index=False,))

@app.route('/view')
def attendance_view():
    data = pd.read_sql('attendance',engine)
    today =datetime.now()
    today_result = ttendance.query.filter(date=today)
    return render_template('attendance.html',data = data.to_html(classes=('table','table-hovered','table-sm','table-responsive'),max_rows=None,max_cols=None,table_id='attendance',index=False,),today_result=today_result)
if __name__=='__main__':
    app.run(debug=True, threaded=True)
