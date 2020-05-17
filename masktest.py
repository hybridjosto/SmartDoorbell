import numpy as np
import cv2
import imutils


def mask_img(img):
    # set up a blank mask array of zeros
    mask = np.zeros((img.shape[0], img.shape[1]), dtype="uint8")

    # load the first polygon
    pts = np.array([[449, 315], [542, 318], [538, 365], [460, 358]])
    cv2.fillConvexPoly(mask, pts, 255)

    # load the second polygon
    pts = np.array([[748, 426], [883, 432], [1018, 504], [
                   916, 539], [898, 647], [827, 621], [838, 517]])

    cv2.fillConvexPoly(mask, pts, 255)

    masked = cv2.bitwise_and(img, img, mask=mask)

    grey = imutils.resize(masked, width=200)

    grey = cv2.cvtColor(grey, cv2.COLOR_BGR2GRAY)

    grey = cv2.GaussianBlur(grey, (11, 11), 0)

    return masked, grey


picFolder = r'/home/pi/SmartDoorbell/Pics/camera_location.jpg'
image = cv2.imread(picFolder)
cv2.imshow('image', image)
cv2.waitKey()
#mask_img(file)
