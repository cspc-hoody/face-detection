import cv2
import numpy as np
from PIL import Image
import os

path = '../face-detection-data/userdata'
detector = cv2.CascadeClassifier("D:\python\Cascade\haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create() #LBP알고리즘을 이용하기 위한 새 변수를 생성

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,file) for file in os.listdir(path)]#이미지 파일들을 안에 넣음
    faceSamples=[] #각 이미지의 얼굴 값을 array uint8 형태로 저장한것을 dictionary 형태로 저장
    ids = [] #여러개의 id값을 배열로 저장
    for imagePath in imagePaths: #이미지 파일을 하나씩 받아 옴
        PIL_img = Image.open(imagePath) #image를 grayscale로 변환 시킨다고 함 (굳이..? 이미 되어있는데)
        img_numpy = np.array(PIL_img,'uint8') #np.array로 img 파일을 int형으로 변환시켜 저
        id = int(os.path.split(imagePath)[-1].split("_")[1])#파일의 id를 추출
        faces = detector.detectMultiScale(img_numpy)#다시 얼굴 이미지에서 또 얼굴을 추출 (얼굴의 크기를 알기 위함)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])#img를 int형으로 바꾼 sample들을 넣은 배열
            ids.append(id)#id값을 쭉 넣어서 배열로 만듦
    return faceSamples, ids
print("\nPlease wait for a second...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids)) #LBP matrix를 만듦. 이에 대한 추가설명은 블로그

recognizer.write('trainer/trainer.yml') #만든 LBP matrix를 yml 파일 형태로 저장
print("\n {0} faces trained.\n".format(len(np.unique(ids))))#ids 배열의 개수만큼 훈련되었다고 표시함.
