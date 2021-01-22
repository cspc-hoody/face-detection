import cv2
import numpy as np
import os
import serial
import time
# Arduino setup Serial Monitor
ser = serial.Serial('com8', 9600)
time.sleep(2) #delay because of serial communication


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
detector = cv2.CascadeClassifier("D:\python\Cascade\haarcascade_frontalface_default.xml")
font = cv2.FONT_HERSHEY_SIMPLEX #opencv에서 지원하는 font

id = 0

#Setting before data by text file
names = []
in_lab_set = set()
f_read = open('user_name.txt', 'r')
print("User Data\n")
while True:
    f_name = f_read.readline()
    if not f_name: break
    f_name = f_name.rstrip('\n')
    print(f_name)
    names.append(f_name)
f_read.close()
f_read = open('R914_lab_user.txt', 'r')
while True:
    f_name = f_read.readline()
    if not f_name: break
    f_name = f_name.rstrip('\n')
    in_lab_set.add(f_name)
f_read.close()

#etting Video
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

in_lab_list = [0]
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(
        gray,
        scaleFactor = 1.05,
        minNeighbors = 8,
        minSize = (20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255), 2)
        #predict에 대한 설명은 blog
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        if (confidence < 55):
            id_num = str(id)
            id = names[id]
            in_lab_list[0] = id
            in_lab_set_compare = set(in_lab_list)
            in_lab_set_compare = in_lab_set_compare & in_lab_set
            if not in_lab_set_compare:
                ser.write(id_num.encode())
                f_write = open('R914_lab_user.txt', 'a')
                in_lab_set.add(id)
                f_write.write(str(id) + '\n')
                f_write.close()
                #if ser.readable():
                #    res = ser.readline()
                #    print(res.decode()[:len(res)-1])

            confidence = " {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = " {0}%".format(round(100 - confidence))
        #일치 확률과 이름을 화면에 출력
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (0,255,0),2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (0,255,0),2)

    cv2.imshow('camera',img)
    #최대한 자주 Key를 획득할 수 있도록 wait time을 줄임
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

print("\nExisting Program.")
f_write = open('R914_lab_user.txt', 'w') #initialize dataset
f_write.close()
cap.release()
cv2.destroyAllWindows()
