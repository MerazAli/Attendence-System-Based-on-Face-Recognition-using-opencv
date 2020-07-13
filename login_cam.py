
import cv2
import numpy as np
import os
import pickle
from database_orm import Attendance
def load_model():
    model=cv2.face.LBPHFaceRecognizer_create()
    return model.read('ai.xml')

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
    pass
