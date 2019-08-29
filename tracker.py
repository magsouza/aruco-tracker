import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib as mpl
import matplotlib.pyplot as plt

class Tracker:

    def __init__(self, mtx, dst):
        self.focal = mtx
        self.distortion = dst
    
    def run(self, ftype, name):
        if ftype == 'video':
            self.run_video(name)
        elif ftype == 'photo':
            self.run_photo(name)
    
    def run_video(self, name):
        # captures the video
        cap = cv2.VideoCapture(name)

        # while video is running
        while (cap.isOpened()):

            # get frame
            ret, frame = cap.read()

            # last frame
            if(not frame):
                break

            # aruco dict paramenters, corners and ids
            aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
            parameters = aruco.DetectorParameters_create()
            corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

            # vector to estimate pose
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.1, self.focal, self.distortion)

            if ids.size > 0:
                # draws axis on the markers
                for i in range(ids.size):
                    aruco.drawAxis(frame, self.focal, self.distortion, rvec[i], tvec[i], 0.1)

                # makes drawnings on the markers
                frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

                cv2.imshow('My video', frame_markers)

            else:
                print("No IDs detected")
                cv2.imshow('My video', frame)

            k = cv2.waitKey(1) & 0xff

            if (k == 27):
                break

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

        # vectors to pose estimation
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, self.focal, self.distortion)

        for i in range(ids.size):
            print(f'id = {ids[i]}')
            print(f'rvec = {rvec[i][0]}')
            print(f'tvec = {tvec[i][0]}')

        if ids.size > 0:
            # draws axis on the markers
            for i in range(ids.size):
                aruco.drawAxis(img, self.focal, self.distortion, rvec[i], tvec[i], 0.1)

            # makes drawnings on the markers
            img_markers = aruco.drawDetectedMarkers(img.copy(), corners, ids)
            
            hig = int(img_markers.shape[0] * 0.75)
            wid = int(img_markers.shape[1] * 0.75)
            img_markers = cv2.resize(img_markers, (hig, wid))
            
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