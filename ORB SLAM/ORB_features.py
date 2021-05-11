'''
ORB Feature Extraction
TODO
1. Feature Matching
- 2 image
- ORB Feature
- Brute Force Matcher

2. KeyFrame
- Frame with matches points

3. Tracking Position (PnP)
- Matrix of intrinsic camera
- Matches points (use RANSAC to eliminate outliers point)

4. Covisibility

5. Mapping
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('../data/ORB/orb1.jpg')
img2 = cv2.imread('../data/ORB/orb1.jpg')
img_width = 640 # An assumption
img_height = 480
img_size = ((img_height,img_width))
img = cv2.resize(img,img_size,interpolation=cv2.INTER_AREA)
img2 = cv2.resize(img2,img_size,interpolation=cv2.INTER_AREA)

# Intrinsic Camera
'''
SHOULD BE CALIBRATED!!
'''
kinect_intrinsic_param = np.array([[514.04093664, 0., 320], [0., 514.87476583, 240], [0., 0., 1.]])
kinect_distortion_param = np.array([2.68661165e-01, -1.31720458e+00, -3.22098653e-03, -1.11578383e-03, 2.44470018e+00])

# applying homography matrix as inference of perpective transformation
def output_perspective_transform(img_object, M):
    print(img_object.shape)
    h,w,_ = img_object.shape
    corner_pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    center_pts = np.float32([ [w/2,h/2] ]).reshape(-1,1,2)
    corner_pts_3d = np.float32([ [-w/2,-h/2,0],[-w/2,(h-1)/2,0],[(w-1)/2,(h-1)/2,0],[(w-1)/2,-h/2,0] ])###
    corner_camera_coord = cv2.perspectiveTransform(corner_pts,M)###
    center_camera_coord = cv2.perspectiveTransform(center_pts,M)
    return corner_camera_coord, center_camera_coord, corner_pts_3d, center_pts

# solving pnp using iterative LMA algorithm
def iterative_solve_pnp(object_points, image_points):
    image_points = image_points.reshape(-1,2)
    retval, rotation, translation = cv2.solvePnP(object_points, image_points, kinect_intrinsic_param, kinect_distortion_param)
    return rotation, translation

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


# Init list of points to save points coordinates
points1 = np.zeros((len(matches), 2), dtype=np.float32)
points2 = np.zeros((len(matches), 2), dtype=np.float32)

for i, match in enumerate(matches):
    points1[i, :] = kp1[match.queryIdx].pt    #gives index of the descriptor in the list of query descriptors
    points2[i, :] = kp2[match.trainIdx].pt    #gives index of the descriptor in the list of train descriptors

'''
Find Homography using RANSAC
Output = matrix Homography
'''
h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

# apply homography matrix using perspective transformation
corner_camera_coord, center_camera_coord, object_points_3d, center_pts = output_perspective_transform(img_fix, h)
        
# solve pnp using iterative LMA algorithm
rotation, translation = iterative_solve_pnp(object_points_3d, corner_camera_coord)

print(f"[INFO] ROTATION =\n{rotation}\nTRANSLATION =\n{translation}")

cv2.waitKey()
cv2.destroyAllWindows()