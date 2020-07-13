
import cv2
import numpy as np
import os
import pickle
from database_orm import Attendance
def load_model():
    model=cv2.face.LBPHFaceRecognizer_create()
    return model.read('models/ai.xml')

#function to detect face using OpenCV
def detect_face(img,cascade = 'cascades/lbpcascade_frontalface.xml'):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cascade)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
    if (len(faces) == 0):
        return None, None
    
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]

def predict(test_img,face_recognizer):
    img = test_img.copy()
    try:
        face, rect = detect_face(img)
        label= face_recognizer.predict(face)[0]
        print(label)
        label_text = subjects[label]
        draw_rectangle(img, rect)
        draw_text(img, label_text, rect[0], rect[1]-5)
        return img, label, label_text
    except Exception as e:
        print(e)
        return img ,None,None

def webcam(sess,path='cascades/haarcascade_frontalface_default.xml',scale=1.3,neighbors=5,pad=20,limit=30 ):
    cap=cv2.VideoCapture(0) 
    face_recognizer = load_model()
    while True:
        status, frame=cap.read()
        w=int(cap.get(3))
        h=int(cap.get(4))
        xstart=int(w//2)
        yend=int(h//2)
        font=cv2.FONT_HERSHEY_SIMPLEX
        if status:
            frame=cv2.flip(frame,3) 
            uframe,label, label_text = predict(frame,face_recognizer)
            if label_text and label:
                print("taking attendace,closing camera")
                roll = int(label_text.split('_')[1])
                attendance = Attendance(roll=roll)
                sess.add(attendance)
                sess.commit()
                return True
            cv2.imshow("login camera",uframe)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                return False
        else:
            return False                                                                                                           
    cap.release()
    cv2.destroyAllWindows()    

if __name__ == "__main__":
    print("Predicting images...")

    model=cv2.face.LBPHFaceRecognizer_create()
    face_recognizer =  model.read('models/ai.xml')

    
    #load test images
    test_img1 = cv2.imread("dataset\\meraz_123\\meraz_8.jpg")
    test_img2 = cv2.imread("dataset\\shahbaz_456\\shahbaz_20.jpg")

    #perform a prediction
    img1, label1, label_text1 = predict(test_img1,face_recognizer)
    cv2.imshow(str(label1),img1)
    img2, label2, label_text2 = predict(test_img2,face_recognizer)
    cv2.imshow(str(label2), img2)
    print("Prediction complete")

    #display both images
    cv2.waitKey(0)
    cv2.destroyAllWindows()
