import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


################################################################################
################################ MOVE ELSEWHERE ################################
# Pre-process the piece
def identify_contour(piece, threshold_low=99, threshold_high=255):
    """Identify the contour around the piece"""
    piece = cv.cvtColor(piece, cv.COLOR_BGR2GRAY)  # better in grayscale
    ret, thresh = cv.threshold(piece, threshold_low, threshold_high, 0)
    contours, hiers = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour_sorted = np.argsort(list(map(cv.contourArea, contours)))
    return contours, contour_sorted[-2]


def get_bounding_rect(contour):
    """Return the bounding rectangle given a contour"""
    x, y, w, h = cv.boundingRect(contour)
    return x, y, w, h


def draw_params(matches_mask=None):
    return dict(matchColor=(0, 0, 255),  # draw matches in green color
                singlePointColor=(255, 0, 0),
                matchesMask=matches_mask,  # draw only inliers
                flags=cv.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

################################################################################
################################################################################


# LOAD IMAGES
img_jigsaw = cv.imread('jigsaw_examples/1000_tropics_jigsaw/jig-tropics-3.jpg')
img_piece = cv.imread('jigsaw_examples/1000_tropics_jigsaw/piece_4.jpg')

# Get the contours
contours, contour_index = identify_contour(img_piece.copy())

# Get a bounding box around the piece
x, y, w, h = get_bounding_rect(contours[contour_index])
img_piece = img_piece.copy()[y:y + h, x:x + w]


print("Cropped piece to bounding box")

# Initiate SIFT detector
orb = cv.ORB_create(nfeatures=100000, scoreType=cv.ORB_HARRIS_SCORE, edgeThreshold=20, scaleFactor=1.5)

# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img_piece, None)
kp2, des2 = orb.detectAndCompute(img_jigsaw, None)


# create BFMatcher object
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1, des2)

# Sort them in the order of their distance.
matches = sorted(matches, key=lambda x: x.distance)

# Draw first 10 matches.
img3 = cv.drawMatches(img_piece, kp1, img_jigsaw, kp2, matches[:10], outImg=None, **draw_params())


# # RESIZE & SHOW RESULTS
width = int(1400)
height = int(1000)
dim = (width, height)
resized = cv.resize(img3, dim, interpolation=cv.INTER_AREA)

cv.imshow('sift_keypoints.jpg', resized)
cv.waitKey(0)
