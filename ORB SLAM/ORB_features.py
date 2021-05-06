'''
ORB Feature Extraction
TODO
1. Feature Matching
2. KeyFrame
3. Tracking Position
4. Covisibility
5. Mapping
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('../data/ORB/orb1.jpg')
img2 = cv2.imread('../data/ORB/orb2.jpg')
img_width = 640 # An assumption
img_height = 480
img_size = ((img_height,img_width))
img = cv2.resize(img,img_size,interpolation=cv2.INTER_AREA)
img2 = cv2.resize(img2,img_size,interpolation=cv2.INTER_AREA)

# Initiate ORB detector
orb = cv2.ORB_create(nfeatures=1000,scaleFactor=1.2)

# compute the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# draw only keypoints location,not size and orientation
img = cv2.drawKeypoints(img, kp1, None, color=(0,255,0), flags=0)
# cv2.imshow("ORB1",img)


print("[INFO] Key Points / Feature = {} {}".format(len(kp1),len(kp2)))
print("[INFO] Descriptor = ", des1.shape, des2.shape)

# create BFMatcher object
bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True)
# Match descriptors.
matches = bf.match(des1,des2)
'''
matches object attributes : 
DMatch.distance - Distance between descriptors. The lower, the better it is.
DMatch.trainIdx - Index of the descriptor in train descriptors (new image)
DMatch.queryIdx - Index of the descriptor in query descriptors (last image)
DMatch.imgIdx - Index of the train image.
'''
# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)
# Draw first 10 matches.
img3 = cv2.drawMatches(img,kp1,img2,kp2,matches[:10],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imshow("Matches",img3)

print("[INFO] Match Points = {}".format(len(matches)))
idx = list()
for i in range(10):
    idx.append(matches[i].trainIdx)

kp_connected = list()
print(len(kp2))

for i in range(len(kp2)):
    if i in idx:
        kp_connected.append(kp2[i])

print(len(kp_connected))

img_fix = cv2.drawKeypoints(img2, kp_connected, None, color=(0,255,0), flags=0)
cv2.imshow("Fixed Connected Points",img_fix)
cv2.waitKey()
cv2.destroyAllWindows()