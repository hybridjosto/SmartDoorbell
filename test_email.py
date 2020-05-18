
import os
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# print(" sdfs")

# define timestamp
pic_time = datetime.now().strftime('%Y%m%d%H%M%S')
command = 'raspistill -w 1280 -h 740 -o '+ pic_time +'.jpg'

os.system(command)

# Gmail login information
smtpUser = 'hybridjosto699@gmail.com'
smtpPass = 'tvtc qlql ztwt ubty'

# To/from information
toAdd = 'josh.stockwell@me.com'
fromAdd = smtpUser
subject = 'Ring recording from: ' + pic_time 
msg = MIMEMultipart()
msg['Subject'] = subject
msg['From'] = fromAdd
msg['To'] = toAdd
msg.preamble = "Photo @ " + pic_time

# Email Text
body = MIMEText ("Image recorded at " + pic_time)
msg.attach(body)

# Attach image
fp = open(pic_time + '.jpg','rb')
img = MIMEImage(fp.read())
fp.close()
msg.attach(img)

#Send email
s = smtplib.SMTP('smtp.gmail.com', 587)

s.ehlo()
s.starttls()
s.ehlo()

s.login(smtpUser, smtpPass)
s.sendmail(fromAdd, toAdd, msg.as_string())
s.quit()

print("Email has been sent")

