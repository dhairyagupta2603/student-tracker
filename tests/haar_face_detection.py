import os

import numpy as np
import cv2

script_dir = os.path.dirname(os.path.abspath(__file__))
cascade_path = os.path.join(script_dir, 'Cascades/haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier(cascade_path)
print(cv2.data.haarcascades)

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height


while(True):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        img,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )

    pad = 70
    for (x,y,w,h) in faces:
        cv2.rectangle(img,
                      (x - pad, y - pad), 
                      (x+w + pad,y+h + pad), 
                      (255,0,0), 
                      2)
        # roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w] 
    
    cv2.imshow('frame', img)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
cap.release()
cv2.destroyAllWindows()