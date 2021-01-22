import numpy as np
import cv2
# Cascades 디렉토리의 haarcascade_frontalface_default.xml 파일을 Classifier로 사용
# faceCascade는 이미 학습 시켜놓은 XML 포멧이고, 이를 불러와서 변수에 저장함.
faceCascade = cv2.CascadeClassifier('D:\python\Cascade\haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('D:\python\Cascade\haarcascade_eye.xml')
smileCascade = cv2.CascadeClassifier('D:\python\Cascade\haarcascade_smile.xml')
# 비디오의 setting을 준비함.
cap = cv2.VideoCapture(0) #0번이 내장카메라, 1번이 외장카메라
cap.set(3,640) # set Width
cap.set(4,480) # set Height
#cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)

while True:
    # video의 이미지를 읽어옴
    ret, img = cap.read()
    #img = cv2.flip(img, 1) # 상하반전
    # 이후 얼굴을 검출할 gray scale을 만듦
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #make grayscale
    roi_gray = gray
    roi_color = img
    faces = faceCascade.detectMultiScale( #이미지에서 얼굴을 검출
        gray, #grayscale로 이미지 변환한 원본.
        scaleFactor=1.2, #이미지 피라미드에 사용하는 scalefactor
        #scale 안에 들어가는 이미지의 크기가 1.2씩 증가 즉 scale size는 그대로
        # 이므로 이미지가 1/1.2 씩 줄어서 scale에 맞춰지는 것이다.
        minNeighbors=3, #최소 가질 수 있는 이웃으로 3~6사이의 값을 넣어야 detect가 더 잘된다고 한다.
        #Neighbor이 너무 크면 알맞게 detect한 rectangular도 지워버릴 수 있으며,
        #너무 작으면 얼굴이 아닌 여러개의 rectangular가 생길 수 있다.
        #만약 이 값이 0이면, scale이 움직일 때마다 얼굴을 검출해 내는 rectangular가 한 얼굴에
        #중복적으로 발생할 수 있게 된다.
        minSize=(20, 20) #검출하려는 이미지의 최소 사이즈로 이 크기보다 작은 object는 무시
        #maxSize도 당연히 있음.
    )
    for (x,y,w,h) in faces: #좌표 값과 rectangular의 width height를 받게 된다.
        #x,y값은 rectangular가 시작하는 지점의 좌표
        #원본 이미지에 얼굴의 위치를 표시하는 작업을 함.
        #for문을 돌리는 이유는 여러 개가 검출 될 수 있기 때문.
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
        #다른 부분, 얼굴 안에 들어있는 눈과 입 등을 검출할 때 얼굴 안엣 검출하라는 의미로 이용되는 것
        roi_gray = gray[y:y+h, x:x+w] #눈,입을 검출할 때 이용
        roi_color = img[y:y+h, x:x+w] #눈,입등을 표시할 때 이용

    eyes = eyeCascade.detectMultiScale(
        roi_gray,
        scaleFactor = 1.2,
        minNeighbors = 10,
        minSize=(3, 3),
    )
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0,0,0), 2)

    smile = smileCascade.detectMultiScale(
        roi_gray,
        scaleFactor = 1.5,
        minNeighbors = 15,
        minSize=(20, 20),
    )
    for (sx, sy, sw, sh) in smile:
        cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0,0,255), 2)

    #영상에 img 값을 출력
    cv2.imshow('video',img) # video라는 이름으로 출력
    k = cv2.waitKey(1) & 0xff #time값이 0이면 무한 대기, waitKey는 키가 입력 받아 질때까지 기다리는 시간을 의미한다.
    #FF는 끝의 8bit만을 이용한다는 뜻으로 ASCII 코드의 0~255값만 이용하겠다는 의미로 해석됨. (NumLock을 켰을때 또한 )
    if k == 27: # press 'ESC' to quit # ESC를 누르면 종료
        break
cap.release() #비디오 끄기   (카메라 리소스 헤제)
cv2.destroyAllWindows()
