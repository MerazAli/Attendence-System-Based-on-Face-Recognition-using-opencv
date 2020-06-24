import cv2


def register_cam(folder,name, path='cascades/haarcascade_frontalface_default.xml',scale=1.3,neighbors=5,pad=20,limit=30 ):
    cap=cv2.VideoCapture(0) 
    face_cascade = cv2.CascadeClassifier(path)

    count=0
    while True:
        status, frame=cap.read()
        w=int(cap.get(3))
        h=int(cap.get(4))
        xstart=int(w//2)
        yend=int(h//2)
        font=cv2.FONT_HERSHEY_SIMPLEX
        if status:
            frame=cv2.flip(frame,3) 
            gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scale, neighbors)
            
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x-pad,y-pad),(x+w+pad,y+h+pad),(255,0,0),2)
                roi_gray = gray[y-pad:y+h+pad, x-pad:x+w+pad]
                cv2.imshow("roi",roi_gray)
                cv2.imshow("frame",frame)
            # add a text message to tell press c to capture and register image --meraz 
            # save image in dataset
            try:
                count+=1
                cv2.imwrite(folder+'/'+name + '_' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            except:
                pass
            if count == limit:
                break
            if cv2.waitKey(1) & 0xFF == ord('c'):
                break
        else:
            break                                                                                                              
    cap.release()
    cv2.destroyAllWindows()    

if __name__ == "__main__":
    pass