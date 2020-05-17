import numpy as np
import cv2
import imutils
import time
import os

picFolder = '/home/pi/SmartDoorbell/Pics/'
vidFolder = '/home/pi/SmartDoorbell/Video/'


def mask_img(img):

    mask = np.zeros((img.shape[0], img.shape[1]), dtype="uint8")

    pts = np.array([[449, 315], [542, 318], [538, 365], [460, 358]])
    cv2.fillConvexPoly(mask, pts, 255)

    pts = np.array([[748, 426], [883, 432], [1018, 504], [
                   916, 539], [898, 647], [827, 621], [838, 517]])
    cv2.fillConvexPoly(mask, pts, 255)

    masked = cv2.bitwise_and(img, img, mask=mask)

    grey = imutils.resize(masked, width=200)

    grey = cv2.cvtColor(grey, cv2.COLOR_BGR2GRAY)

    grey = cv2.GaussianBlur(grey, (11, 11), 0)

    return masked, grey


# Counter Variable for analysis
counter = 0

while True:
    counter = counter + 1
    print ("  ")
    print ("---- Times through loop since starting:" + str(counter) + " ----")
    print ("  ")

    # take 1st and 2nd image to compare

    command = 'raspistill -w 1280 -h 720 -vf -hf -t 1000 -tl 1000 -o ' + picFolder + 'test%0d.jpg'

    os.system(command)

    print ("Captured First and Second Img for Analysis")

    # mask images
    test1 = cv2.imread(picFolder + "test0.jpg")
    test2 = cv2.imread(picFolder + "test1.jpg")

    masked1, grey1 = mask_img(test1)
    masked2, grey2 = mask_img(test2)

    # Compare the two images
    pixel_thres = 50

    detector_total = np.uint64(0)
    detector = np.zeros((grey2.shape[0], grey2.shape[1]), dtype="uint8")

    # Pixel by Pixel comp
    for i in range(0, grey2.shape[0]):
        for j in range(0, grey2.shape[1]):
            if abs(int(grey2[i, j]) - int(grey1[i, j])) > pixel_thres:
                detector[i, j] = 255

    # sum the detector array
    detector_total = np.uint64(np.sum(detector))
    print ("detector total =", detector_total)

    if detector_total > 30000:
        print ("SmartDoorbell has detected something!")

        # define a unique name for the videofile
        timestr = time.strftime("doorbell-%Y%m%d-%H%M%S")

        command2 = 'raspivid -t 10000 -w 1280 -h 720 -vf -hf -fps 30 -o ' + vidFolder + timestr + '.h264'
        os.system(command2)

        print("Finished recording, converting to mp4...")

        command3 = 'MP4Box -fps 30 -add ' + timestr + '.h264 ' + timestr + '.mp4'
        # os.system(command3)

        print("Finished converting file, available for review")

        # write masked images to file
        cv2.imwrite(picFolder + "grey1.jpg", grey1)
        cv2.imwrite(picFolder + "grey2.jpg", grey2)
        cv2.imwrite(picFolder + "masked1.jpg", masked1)
        cv2.imwrite(picFolder + "masked2.jpg", masked2)
    else:
        print("Nothing detected yet...")
