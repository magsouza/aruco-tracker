import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib as mpl
import matplotlib.pyplot as plt

class Tracker:

    def run(self, ftype, name):
        if ftype == 'video':
            self.run_video(name)
        elif ftype == 'photo':
            self.run_photo(name)
    
    def run_video(self, name):
        # captures the video
        cap = cv2.VideoCapture(name)
        points = []

        out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640,480))
        # while video is running
        while (cap.isOpened()):

            # get frame
            ret, frame = cap.read()

            # last frame
            if(frame is None):
                break

            # aruco dict paramenters, corners and ids
            aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
            parameters = aruco.DetectorParameters_create()
            corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

            pos =-1
            for i in range(ids.size):
                if ids[i] == 8:
                    pos = i
                    break
            if 8 in ids:
                c = self.get_center(corners[pos][0])
                points.append(c)
                
            for cent in points:
                cv2.circle(frame, cent, 13, (60,179,113), -1)
            if ids.size > 0:
                # makes drawnings on the markers
                frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)
                out.write(frame_markers)
                cv2.imshow('My video', frame_markers)

            else:
                print("No IDs detected")
                cv2.imshow('My video', frame)

            k = cv2.waitKey(1) & 0xff

            if (k == 27):
                break
        out.release()
        cap.release()
        cv2.destroyAllWindows()

        return

    def run_photo(self, name):
        img = cv2.imread(name)

        # aruco dict paramenters, corners and ids
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
        img_markers = aruco.drawDetectedMarkers(img.copy(), corners, ids)

        if ids.size > 0:
            # makes drawnings on the markers
            img_markers = aruco.drawDetectedMarkers(img.copy(), corners, ids)
            
            cv2.imshow('My photo', img_markers)

        else:
            print("No IDs detected")
            cv2.imshow('My photo', img)

        while(True):
            k = cv2.waitKey(1) & 0xff
            if (k == 27):
                break
        cv2.destroyAllWindows()
        
        return
    
    def get_center(self, corners):
        xm = ym = 0
        for i in range(4):
            xm += corners[i][0]
            ym += corners[i][1]
        
        xm //= 4
        ym //= 4

        return (int(xm), int(ym))