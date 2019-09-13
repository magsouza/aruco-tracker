import numpy as np
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt

class Tracker:

    def __init__(self):
        self.marker_cm = 2.75
        self.marker_px = 0
        self.get_marker = False
        self.desloc = 0
        self.trajetory = []
        self.time = []

    def run(self, name):
        # captures the video
        cap = cv2.VideoCapture(name)

        # plane where the marker falls 
        pts_src = np.array([ [764, 144], [1166, 162], [1191, 766], [721, 766] ])

        # plane where I want the marker
        pts_dst = np.array([ [0, 0], [400, 0], [400, 600], [0, 600] ])            

        # homography
        h , status = cv2.findHomography(pts_src, pts_dst)

        # while video is running
        while (cap.isOpened()):

            # get frame
            ret, frame = cap.read()
       
            # last frame
            if(frame is None):
                break

            # click ESC to quit
            k = cv2.waitKey(1) & 0xff
            if (k == 27):
                break


            frame = cv2.warpPerspective(frame, h, (400, 600))
            cv2.imshow('Clean video', frame)

            # aruco dict paramenters, corners and ids
            aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
            parameters = aruco.DetectorParameters_create()
            corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

            if ids is not None:

                # find marker position and marker size in pixel
                pos = 0
                for i in range(ids.size):
                    # this condition checks the marker size
                    if ids[i] == 9 and not self.get_marker:
                        self.marker_px = abs(corners[i][0][0][0] - corners[i][0][2][0])
                        # comment the next line to get the size of the last frame
                        self.get_marker = not self.get_marker
                    # this condition finds the cube marker
                    if ids[i] == 9:
                        pos = i

                if 9 in ids:
                    c = self.get_center(corners[pos][0])
                    self.trajetory.append(c)
                    # as the slow motion is 10x slower
                    self.time.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 10000)

                # draw the circle
                for center in self.trajetory:
                    cv2.circle(frame, center, 5, (255,102,102), -1)
                
                # makes drawnings on the markers
                frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)
                cv2.imshow('Video with tracking', frame_markers)

        cap.release()

        # estimate the displacement of the cube
        self.get_move(self.trajetory)
        
        # coverts from pixel to cm
        self.convert(self.desloc)
     
        cv2.destroyAllWindows()

        fl = self.write_file(self.trajetory, self.time)
        return fl

    def get_center(self, corners):
        xm = ym = 0
        for i in range(4):
            xm += corners[i][0]
            ym += corners[i][1]
        
        xm //= 4
        ym //= 4

        return (int(xm), int(ym))
    
    def get_move(self, points):
        for i in range(1, len(points)):
            x = pow((points[i-1][0] - points[i][0]),2)
            y = pow((points[i-1][1] - points[i][1]),2)
            self.desloc += np.sqrt(x + y)

    def convert(self, v):
        v *= (self.marker_cm / self.marker_px)

    def write_file(self, centers, times):
        f = open('position.txt', 'w+')
        for i in range(len(centers)):
            f.write(f'{centers[i][0]} {centers[i][1]} {times[i]}\n')
        f.close()