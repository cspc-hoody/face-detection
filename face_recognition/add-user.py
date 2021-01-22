import numpy as np
import cv2

f_read = open('user_count.txt', 'r')
user_count = int(f_read.readline())
print("Register User :",user_count)
f_read.close()
#데이터베이스에 올릴  이름과 id를 입력받음
user_name = input("Please write your name : ")
f_write = open('user_name.txt', 'a')
f_write.write(user_name+'\n')
f_write.close()
user_id = user_count + 1
f_write = open('user_count.txt', 'w')
f_write.write(str(user_id))
f_write.close()
detected_data = cv2.CascadeClassifier('D:\python\Cascade\haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
interrupt_flag = 0 # ESC를 입력했을 경우에 flag가 활성화 됨
count = 0
while True:
    ret, img = cap.read()
    #img = cv2.flip(img, 1) # 상하반전
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detected_data.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=9, #조금 더 확실하게 검출하기 위해 Neighbor 값을 증가시킴
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
        count+=1 # 총 100장의 사진을 찍게 되는데, 하나를 찍을 때마다 count가 늘어난다.
        #imwrite를 통해서 이미지를 저장한다. 이때 저장되는 이미지는 _로 나뉘어지며, grayscale 이미지가 저장된다.
        cv2.imwrite("../face-detection-data/userdata/User_"+str(user_id)+'_'+str(user_name)+'_'+str(count)+'.jpg', gray[y:y+h,x:x+w])
        cv2.imshow('image', img) #이미지가 찍힐때 마다 찍힌 사진이 출력되어 보여준다. video가 나오지 않고 이미지로 나온다.
    k = cv2.waitKey(50) & 0xff # waitkey안의 time을 늘리면 조금 더 느리게 찍힌다.
    if k == 27: # press 'ESC' to quit # ESC를 누르면 종료
        interrupt_flag = 1
        break
    elif count >= 100: #100장의 이미지를 모두 찍으면 종료한다.
        break

if interrupt_flag == 1:
    print("\nFinish by interrupt ESC.\n")
else :
    print("\nComplete to save data.\n")


cap.release()
cv2.destroyAllWindows()
