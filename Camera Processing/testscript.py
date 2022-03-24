import numpy as np
import cv2
import copy
import sys
import time
from undistort import undistort
#from square_decision as square_decision
from matplotlib import pyplot as plt
from PIL import Image
import datetime


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    #print("What the fuck")
    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cap.read()
        #if not ret:
         #   print("failed to grab frame")
          #  continue
        frame = undistort(frame)
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cap.release()

    cv2.destroyAllWindows()