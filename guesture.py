import cv2

cap=cv2.VideoCapture(0)     # access ur camera  

bgm=cv2.createBackgroundSubtractorKNN() # quared distance between the pixel and the sample to decide . whether a pixel is close to that sample. This parameter does not affect the background update.

while True:
    status, frame=cap.read()
    w=int(cap.get(3))
    h=int(cap.get(4))
    xstart=int(w//2)
    yend=int(h//2)
    font=cv2.FONT_HERSHEY_SIMPLEX

    if status:
        frame=cv2.flip(frame,3)      # brief Flips a 2D array around vertical, horizontal, or both axes.
        frame=cv2.rectangle(frame,(xstart-125,100),(xstart+125,yend+125),(0,0,0),2)
        frame=cv2.putText(frame,'Face stored in box',(xstart+10,yend-10),font, .5,(255,255,255),1,cv2.LINE_AA)
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("img",frame)
        roi=gray[100:yend+125,xstart-125:xstart+125]
        mask=bgm.apply(roi)
        cv2.imshow("roi",roi)
        cv2.imshow("roimasked",mask)
        if cv2.waitKey(1) & 0xFF == ord('c'):
                # img grab
            print("Capture Face")
        if cv2.waitKey(1) & 0xFF == ord('q'):   # break when q is pressed
            break
    else:
        break                                                                                                              

cap.release()
cv2.destroyAllWindows()    
