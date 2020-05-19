import numpy as np
import cv2
import imutils
import os

firstarray = np.array([[259, 314], [299, 339], [309, 375], [390, 380], [389, 332]])
secondarray = np.array([[729, 420], [977, 410], [1000, 551], 
    [917, 583], [894, 712], [708, 637]])

def mask_img(img):
    # set up a blank mask array of zeros
    mask = np.zeros((img.shape[0], img.shape[1]), dtype="uint8")

    # load the first polygon
    pts = np.array(firstarray)
    cv2.fillConvexPoly(mask, pts, 255)

    # load the second polygon
    pts = np.array(secondarray)

    cv2.fillConvexPoly(mask, pts, 255)

    masked = cv2.bitwise_and(img, img, mask=mask)

    grey = imutils.resize(masked, width=200)

    grey = cv2.cvtColor(grey, cv2.COLOR_BGR2GRAY)

    grey = cv2.GaussianBlur(grey, (11, 11), 0)

    return masked, grey

picFolder = r'/home/pi/SmartDoorbell/Pics/'
command = 'raspistill -w 1280 -h 720 -vf -hf -t 1000 -tl 1000 -o camera_location.jpg'

os.system(command)
image = cv2.imread(picFolder)

def show_results(img):
    imgmod = cv2.polylines(img, [firstarray,secondarray], True, (255,120,255),1)
    cv2.imshow('image', imgmod)
    cv2.waitKey()

show_results(image)    


