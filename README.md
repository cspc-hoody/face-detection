# face-detection

* Team Name HOODY
* developer : 김수민, 김하늘, 황동준

This program is face-detection program that can know about attender of lab
There are 3 executable files in face-detection directory
* add-user.py
add user of face-detection program. If user add in data, user name is written in user_list.txt

* face_recog.py
face-detect and send information of attender to R914_lab_user.txt

* print_name/print_name.ino
This arduino code print name of detected face. I will explain detail at the bottom.

If you want to run this program, try to install library by this command.
```
pip install -r requirements.txt

or

pip3 install -r requirements.txt
```

Only add-user.py and face_recog.py is runnable by python like this.
```
python add-user.py
python face_recog.py

or

python add-user.py
python face_recog.py
```


# PROJECT EXPLANATION
## 1. 개요
랩실안에 누가 있는지 쉽게 파악하기 위해 만든 프로그램이다.
핸드폰 잠금화면처럼, 랩실에 들어오기 전에 들어오려는 사람의 얼굴을 인식하여
만약 랩원이라면 출석자 명단에 포함시키고, 아두이노로 환영 메세지를 보낸다.
출석자 명단을 다른 랩원들과 공유하는 방법은 다음 프로젝트에서 진행중이다.

## 2. Haar_Cascade를 이용한 얼굴인식 프로그램
해당 프로젝트는 Haar_Cascade Branch에 존재한다.

### (1) 블로그
이에 대한 설명은 각자의 블로그에 Compact하게 정리해 놓았다.
[황동준 블로그](https://velog.io/@wbsl0427/opencv%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%8B%A4%EC%8B%9C%EA%B0%84-%EC%96%BC%EA%B5%B4%EC%9D%B8%EC%8B%9D-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8-%EB%A7%8C%EB%93%A4%EA%B8%B0)

### (2) 해당 얼굴인식 프로그램의 문제점
일단 정확도가 높지 않다. detectMultiScale의 factor들을 여러 개 바꿔보아도
실제 랩실에서 이용할 수 없을 정도로 정확도가 높지 않았다.
또한 얼굴이 아닌 부분도 얼굴로 잡히게 된다. 뒤에 있는 사물이나 그림자같은 것도 얼굴로 인식하게 될 때도 있다.
이는 Haar_Cascade방법이 grayscale 이미지를 이용해서 해당 이미지가 얼마나 어두운지에 따라 얼굴을 판단하기 때문이다.

## 3. dlib을 이용한 얼굴인식 프로그램
해당 프로젝트는 main branch에 존재한다.

### (1) 얼굴인식 부분 코드 분석 (face_recog.py)
[황동준 블로그](https://velog.io/@wbsl0427/facerecognition%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%97%AC-%EC%96%BC%EA%B5%B4%EC%9D%B8%EC%8B%9D-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8-%EB%A7%8C%EB%93%A4%EA%B8%B0)

### (2) 얼굴 데이터 추출 및 저장하는 코드 분석 (add-user.py)
이 파일을 이용하는 방법은 다음과 같다.
```
실행
-> 동영상이 나오면 SPACE 버튼 누름
-> 찍힌 사진이 3초간 나옴
-> 다시 SPACE를 눌러서 사진을 찍음
-> 이를 총 3번 반복하면 종료되고, knowns에 각 사진이 이름과 함께 저장됨
-> user_list에서 저장한 user이름들을 볼 수 있음

if face_recog.face_count == 3 :
    break

이 count를 3에서 자기가 찍고 싶은 사진의 개수만큼 늘려주면 됨
```


add-user는 원래 존재하는 face_recog 파일에서 encoding하는 모든 부분을 지우고,
face_locations만 들어 갈 수 있도록 최대한 최적화해서 만든 프로그램이다.

기존에 Haar_Cascade에서 이용했던 파일 저장 방법을 불러와서 keyboard에 SPACE가
입력되면 사진이 찍히는 구조를 이용하였다.
```
if key == 32:
    face_recog.get_image()

    def get_image(self):
          frame = self.get_frame()
          for (top, right, bottom, left) in self.face_locations:
              top *= 4
              right *= 4
              bottom *= 4
              left *= 4
              cv2.imwrite("./knowns/"+str(self.face_name)+'_'+str(self.face_count)+'.jpg', frame[top:bottom,left:right])
              # cv2.imshow('image', img)
              self.face_count+=1
              self.time_sleep = 1
```
`time_sleep`은 3초 정도 찍힌 사진을 볼 수 있도록 만든 flag이며,
opencv 라이브러리의 imwrite 함수를 이용해서 파일을 jpg 형태로 저장하였다.

또한 `user list text file`을 따로 만들어, 등록된 유저의 이름을 저장할 수 있도록 하였다.

사진은 총 3장을 찍을 수 있도록 처리했다.
