
import cv2
import numpy as np
import os
from datetime import datetime
import pickle
from database_orm import Attendance

def load_model(path='models/ai.xml'):
    model=cv2.face.LBPHFaceRecognizer_create()
    model.read(path)
    print(model)
    return model

def get_names(folder='dataset'):
    return os.listdir(folder)

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

#function to detect face using OpenCV
def detect_face(img,cascade = 'cascades/lbpcascade_frontalface.xml'):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cascade)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
    if (len(faces) == 0):
        return None, None
    
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]

def predict(test_img):
    img = test_img.copy()
    model = load_model()
    subjects = get_names()
    # try:
    face, rect = detect_face(img)
    label= model.predict(face)[0]
    label_text = subjects[label]
    draw_rectangle(img, rect)
    draw_text(img, label_text, rect[0], rect[1]-5)
    return img, label, label_text
    # except Exception as e:
    #     print(e)
    #     return img ,None,None

def take_attendace(sess,label_text):
    print("taking attendace,closing camera")
    # roll = int(label_text.split('_')[1])
    # data = sess.query(Attendance).filter(roll=roll).filter(date=datetime.now)
    # print(data)
    # if not data:
    attendance = Attendance(roll=roll)
    sess.add(attendance)
    sess.commit()

def webcam(sess,path='cascades/haarcascade_frontalface_default.xml',scale=1.3,neighbors=5,pad=20,limit=30 ):
    cap=cv2.VideoCapture(0) 
    while True:
        status, frame=cap.read()
        w=int(cap.get(3))
        h=int(cap.get(4))
        xstart=int(w//2)
        yend=int(h//2)
        font=cv2.FONT_HERSHEY_SIMPLEX
        if status:
            frame=cv2.flip(frame,3) 
            uframe, label, label_text = predict(frame)
            print(uframe, label, label_text)
            if label_text:
                take_attendace(sess, label_text)
                break
            cv2.imshow("login camera",uframe)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                return False
        else:
            return False                                                                                                           
    cap.release()
    cv2.destroyAllWindows()  
    return True  

if __name__ == "__main__":
    print("Predicting images...")
    
    #load test images
    test_img1 = cv2.imread("dataset\\luffy_123\\luffy_8.jpg")
    test_img2 = cv2.imread("dataset\\\\meraz_21.jpg")

    #perform a prediction
    img1, label1, label_text1 = predict(test_img1)
    cv2.imshow(str(label1),img1)
    img2, label2, label_text2 = predict(test_img2)
    cv2.imshow(str(label2), img2)
    print("Prediction complete")

    #display both images
    cv2.waitKey(0)
    cv2.destroyAllWindows()
