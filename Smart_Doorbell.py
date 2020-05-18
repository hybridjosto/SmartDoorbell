import numpy as np
import cv2
import imutils
import time
import os

import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from emaildetails import smtpUser
import emaildetails

picFolder = '/home/pi/SmartDoorbell/Pics/'
vidFolder = '/home/pi/SmartDoorbell/Video/'

emailUser = emaildetails.smtpUser
emailPass = emaildetails.smtpPass
emailToAdd = emaildetails.toAdd

print("Camera Running - press CTRL C to exit")
Nothing = 0

def mask_img(img):

    mask = np.zeros((img.shape[0], img.shape[1]), dtype="uint8")

    pts = np.array([[259, 314], [299, 339], [309, 375], [390, 380], [389, 332]])
    cv2.fillConvexPoly(mask, pts, 255)

    pts = np.array([[729, 420], [977, 410], [1000, 551],
                    [917, 583], [894, 712], [708, 637]])
    cv2.fillConvexPoly(mask, pts, 255)

    masked = cv2.bitwise_and(img, img, mask=mask)

    grey = imutils.resize(masked, width=200)

    grey = cv2.cvtColor(grey, cv2.COLOR_BGR2GRAY)

    grey = cv2.GaussianBlur(grey, (11, 11), 0)

    return masked, grey


def emailPics(pic_time):
    print("emailing images")
    # To/from information
    fromAdd = smtpUser
    subject = 'Doorbell recording from: ' + pic_time 
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromAdd
    msg['To'] = emailToAdd
    msg.preamble = "Photo @ " + pic_time

    # Email Text
    body = MIMEText ("Image recorded at " + pic_time)
    msg.attach(body)

    # Attach image
    fp = open('test0'.jpg','rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    fp = open('test1'.jpg','rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    #Send email
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(smtpUser, smtpPass)
    s.sendmail(fromAdd, emailToAdd, msg.as_string())
    s.quit()

    print("Email has been sent")

# Counter Variable for analysis
counter = 0

while True:
    counter = counter + 1
    # print ("  ")
    # print ("---- Times through loop since starting:" + str(counter) + " ----")
    # print ("  ")

    # take 1st and 2nd image to compare

    command = 'raspistill -w 1280 -h 720 -vf -hf -t 1000 -tl 1000 -o ' + picFolder + 'test%0d.jpg'

    os.system(command)

    # print ("Captured First and Second Img for Analysis")

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
    

    if detector_total > 30000:
        print ("SmartDoorbell has detected something!", str(counter))
        print ("detector total =", detector_total)
        # define a unique name for the videofile
        timestr = time.strftime("doorbell-%Y%m%d-%H%M%S")

        command2 = 'raspivid -t 10000 -w 1280 -h 720 -vf -hf -fps 30 -o ' + vidFolder + timestr + '.h264'
        os.system(command2)

        print("Finished recording, converting to mp4...")

        # command3 = 'MP4Box -fps 30 -add ' + timestr + '.h264 ' + timestr + '.mp4'
        # os.system(command3)

        print("Finished converting file, available for review")

        # write masked images to file
        cv2.imwrite(picFolder + "grey1.jpg", grey1)
        cv2.imwrite(picFolder + "grey2.jpg", grey2)
        cv2.imwrite(picFolder + "masked1.jpg", masked1)
        cv2.imwrite(picFolder + "masked2.jpg", masked2)

        emailPics(timestr) 
    else:
        Nothing += 1
