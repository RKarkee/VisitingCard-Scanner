from imagetransforming import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

from PIL import Image
import PIL.Image
from pytesseract import image_to_string
import pytesseract
import re
#import json

 #construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required= True,
        help = "Path to the image to be scanned")
args =vars(ap.parse_args())

#edge detection
image = cv2.imread(args["image"])
#print(image)


ratio = image.shape[0] / 500.0
#print(ratio)

orig = image.copy()
image = imutils.resize(image, height = 500)

#image into gray
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

#show original image and edge detection img
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# to find the contours in our images.

cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
screencnt = None
#print(cnts)

# loop over the contours
for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        #print(peri)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        #print(approx)

        if len(approx) == 4:
                screencnt = approx
                break

#show the contour

#print("Step 2: Find contours of paper")
cv2.drawContours(image, [screencnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# bird eye view
warped = four_point_transform(orig, screencnt.reshape(4, 2) * ratio )
warped = cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255

# cv2.imshow("Original", imutils.resize(orig, height = 650))
imS = cv2.resize(warped, (650, 650))
cv2.imshow("output", imS)
#cv2.imwrite('out/'+ 'Output Image.PNG', imS)
cv2.waitKey(0)

output = pytesseract.image_to_string(PIL.Image.open('out/'+ 'Output Image.PNG').convert("RGB"), lang = 'eng')
print(output)
f = open('details.json', 'w')
f.write(output)
f.close()



#extraction of  limited text from images

#regular expression to find emails
emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", output)
#regular expression to find phone numbers
numbers = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', output)

print(numbers)
print(emails)

for email in emails:
	print('EMAIL :-> ' + email)
	F = open('emails.json','a+')
	F.write('EMAIL :-> ' + email)

for number in numbers:
	print('Phone No. :-> ' + number)
	F = open('emails.json', 'a+')
	F.write('\n Phone No. :-> ' + number)