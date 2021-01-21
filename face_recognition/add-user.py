# face_recog.py

import face_recognition
import cv2
import camera
import os
import numpy as np
import time

class FaceRecog():
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.camera = camera.VideoCamera()

        #self.known_face_encodings = []
        #self.known_face_names = []

        # Load sample pictures and learn how to recognize it.

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

        # count user data
        self.face_count = 0

        # user name
        self.face_name = []

        # time sleep
        self.time_sleep = 0

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

        self.process_this_frame = not self.process_this_frame

        # Display the results
        for (top, right, bottom, left) in self.face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            #font = cv2.FONT_HERSHEY_DUPLEX
            #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame

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

if __name__ == '__main__':
    face_recog = FaceRecog()
    face_recog.face_name = input("Please write your name : ")
    f_write = open('user_list.txt', 'a')
    f_write.write(str(face_recog.face_name) + '\n')
    f_write.close()
    while True:
        frame = face_recog.get_frame()

        if face_recog.time_sleep == 1 :
            time.sleep(3)
            face_recog.time_sleep = 0

        if face_recog.face_count == 3 :
            break
        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        if key == 32:
            face_recog.get_image()

    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')
