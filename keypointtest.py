import numpy as np
import cv2
from matplotlib import pyplot as plt

# Alternative to drawMatches. We can probably use this to find out how to interpret the matches
# Source: https://gist.github.com/isker/11be0c50c4f78cad9549
def draw_matches_on_img2(img1, kp1, img2, kp2, matches, color=None):     
    new_img = np.zeros(img2.shape, type(img2.flat[0]))  
    new_img[0:img2.shape[0],0:img2.shape[1]] = img2

    r = 10
    thickness = 2
    if color:
        c = color
    else: 
        c = np.random.randint(0,256,3) if len(img1.shape) == 3 else np.random.randint(0,256)
    
    
    
    for m in matches:
        cv2.circle(new_img, tuple(np.round(kp2[m.trainIdx].pt).astype(int)), r, c, thickness)

    return new_img

def scalePoints(points, kp1, kp2, matches):
    if len(matches) < 2:
        print("Error, not enough matches. Two Required, %d given\n" % len(matches))
    
    
    # Scale the points from the smaller image to the larger image
    
    # I don't think I need the matches param, but I'll see
    
    #smaller (closer) image is the number 1
    #Idea: take the 1st point from image 1 (should be the best match),
    #    translate all the points to match the corresponding point in image 2.
    #    Then, scale the points from image 1 to match the second corresponding point in image 2.
    #    If there is a lot of error, maybe try the scaling on multiple points and average the scale factor, then apply it
    
    
    #See this!!!: https://math.stackexchange.com/questions/1544147/find-transform-matrix-that-transforms-one-line-segment-to-another
    #There are 3 steps:
    #   Scale
    #      Use distances of points and scale
    #   Rotate
    #      use atan2()
    #      θ=atan2(by−ay,bx−ax)
    #   Translate
    #      Add the value of the original coordinate to all the others
    
    #----------------------------------------Scaling---------------------------------------
    smlPt_0 = kp1[match[0].queryIdx].pt
    bigPt_0 = kp2[match[0].trainIdx].pt
    
    smlPt_1 = kp1[match[1].queryIdx].pt
    bigPt_1 = kp2[match[1].trainIdx].pt
    
    distance1 = ((smlPt_0[0] - smlPt_1[0]) ** 2 + (smlPt_0[1] - smlPt_1[1]) ** 2) ** 0.5
    distance2 = ((bigPt_0[0] - bigPt_1[0]) ** 2 + (bigPt_0[1] - bigPt_1[1]) ** 2) ** 0.5
    
    
    
    #Set the first point of smaller image to origin before rotation
    #-----------------------------------------Translation One-----------------------------------
    smlTranslateBy = kp1[match[0].queryIdx].pt
    smlPt_0 = (0, 0)
    smlPt_1 = (smlPt_1[0] - smlTranslateBy[0], smlPt_1[1] - smlTranslateBy[1]) #generalize to all points eventually
    
    
    
    #Scale all (aside from match 1) points in img1 by scale factor
    #______________________________________________Scale________________________________________
    scale_factor = distance2/distance1
    
    smlPt_1 = (smlPt_1[0] * scale_factor, smlPt_1[1] * scale_factor)

    
    #------------------------------------------Rotate-------------------------------------
    #(1x2)(2x2) =(1x2) img1pts * matrix = bigimgpts
    
    
    #-----------------------------------------Translation Two-----------------------------------
    
    
    
    
    
    
    return points
    
    
    
    return 

def process_matches(img1, kp1, img2, kp2, matches):  
    points = None
    
    #for m in matches:
        #points.append(kp2[m.trainIdx].pt)
    
    points = scalePoints(points, kp1, kp2, matches)
    
    return points



MIN_MATCH_COUNT = 1

img2 = cv2.imread('pic1.jpg')      # queryImage
img1 = cv2.imread('pic1_closer.jpg')             # trainImage

# Initiate SIFT detector
sift = cv2.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)

# store all the good matches as per Lowe's ratio test.
# CONSTANT_TEST Determines sensitivity of whats a good match
# CONSTANT_TEST = 0.7 # <-- Default
CONSTANT_TEST = 0.8 #Testing, seems good. 

good = []
for m,n in matches:
    if m.distance < CONSTANT_TEST*n.distance:
        good.append(m)

print("There are %d good matches" % len(good))
# if len(good)>MIN_MATCH_COUNT:
#     # ERROR with this code vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv This is what was causing the random line
#     src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
#     dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    

#     M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
#     matchesMask = mask.ravel().tolist()
#     h,w = img1.shape[0], img1.shape[1]                  #This line was causing problems, cause the image can be len 3. I modified to fix it
#     pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
#     dst = cv2.perspectiveTransform(pts,M)

#     img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
#     

# else:
#     print( "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
#     # print( "Not enough matches are found")
#     matchesMask = None
    
draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                #    matchesMask = matchesMask, # draw only inliers
                   matchesMask= None,
                   flags = 2)

img3 = cv2.drawMatches(img1, kp1, img2,kp2,good,None,**draw_params)

img4 = draw_matches_on_img2(img1, kp1, img2, kp2, good, color=(255,0,0))


plt.imshow(img4)
print("Press Q to see other/quit")
plt.show()


plt.imshow(img3)
plt.show()
process_matches(img1, kp1, img2, kp2, good)