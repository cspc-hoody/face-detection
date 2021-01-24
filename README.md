# face-detection
출입 시 카메라를 통해 얼굴을 인식하여, 현재 물리적 공간에 상주하고 있는 멤버에 대해 원격으로 알 수 있는 프로그램이다.

* developer : 김수민, 김하늘, 황동준
* 2020.12.27 - 2021.01.21

### 진행 순서
1. Git
2. 머신러닝
3. 1차 시도 OpenCV
4. 2차 시도 dlib
5. 아두이노 연결
6. 카카오톡 채널 서비스 (보류)

# 1. Installation

# 2. How to Execute

# 3. Program Structure

## 3-1. add-user.py
## 3-2. face_recog.py
## 3-3. print_name/print_name.ino

> * Arduino Uno
> * [8x8 LED Matrix 4개](https://www.devicemart.co.kr/goods/view?no=1330850)

* library
[LedControl](https://github.com/wayoda/LedControl)

### How to execute
1. 아두이노 Uno와 8x8 LED Matrix 4개를 연결하고,
2. 아두이노 코드(print_name.ino)를 업로드한다.
3. face_recog.py를 실행시켜, 얼굴을 인식하면 매칭되는 얼굴에 해당하는 이름이 LED Matrix에 출력된다.

### detail
자세한 코드 리뷰 및 구현 시도는 [블로그](https://velog.io/@huttzza/%EC%8B%A4%EC%8B%9C%EA%B0%84-%EC%96%BC%EA%B5%B4-%EC%9D%B8%EC%8B%9D-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8-%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8-%EC%97%B0%EA%B2%B0) 참조