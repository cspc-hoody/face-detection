# face_recog.py

import face_recognition
import cv2
import camera
import os
import numpy as np
import serial
import time

class FaceRecog():
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.camera = camera.VideoCamera()

        self.known_face_encodings = []
        self.known_face_names = []

        # Load sample pictures and learn how to recognize it.
        dirname = 'knowns'
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                try :
                    face_encoding = face_recognition.face_encodings(img)[0]
                except Exception as e :
                    pass
                self.known_face_encodings.append(face_encoding)

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

        # count person who attend lab
        self.in_lab_set = set()
        self.timeList = {}

        f_read = open('user_list.txt', 'r')
        while True:
            user_list_name = f_read.readline()
            if not user_list_name:
                break
            user_list_name = user_list_name.rstrip('\n')
            self.timeList[user_list_name] = [0, 0.0]
        f_read.close()
            

        # Arduino
        self.ser = serial.Serial('com3', 9600)
        time.sleep(2)

    def __del__(self):
        del self.camera

    def get_frame(self):
        # Grab a single frame of video
        frame = self.camera.get_frame()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 0.6 is typical best performance.
                name = "Unknown"
                if min_value < 0.45:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]
                    name = name.split('_')[0]

                    
                    #딜레이
                    key = name
                    flag = self.timeList[key][0]
                    timeStamp = self.timeList[key][1]

                    if timeStamp == 0:
                        self.timeList[key][1] = time.time()
                        if flag == 0:
                            hello_name = "Hello,"+name
                            self.ser.write(hello_name.encode())
                            f_write = open('R914_lab_user.txt', 'a')
                            self.in_lab_set.add(name)
                            print(self.in_lab_set)
                            f_write.write(str(name) + '\n')
                            f_write.close()
                            #스택추가
                        else :
                            bye_name = "Bye,"+name
                            self.ser.write(bye_name.encode())
                            f_write = open('R914_lab_user.txt', 'w')
                            self.in_lab_set.remove(name)
                            print(self.in_lab_set)
                            print(time.time() - timeStamp)
                            f_write.write(str(name) + '\n')
                            f_write.close()
                            #스택 제거
                    elif(time.time() - timeStamp) > 10 :
                        if flag == 0:
                            print("#10초지남나가야댐",name,(time.time() - timeStamp))

                            self.timeList[key][0] = 1
                            self.timeList[key][1] = 0
                        else:
                            print("###",name,(time.time() - timeStamp))
                            self.timeList[key][0] = 0
                            self.timeList[key][1] = 0

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame

    def get_jpg_bytes(self):
        frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


if __name__ == '__main__':
    face_recog = FaceRecog()
    print(face_recog.known_face_names)
    while True:
        frame = face_recog.get_frame()

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')
    f_write = open('R914_lab_user.txt', 'w')
    f_write.close()
