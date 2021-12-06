import numpy as np
import cv2 as cv


# TODO: Move elsewhere
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
sift = cv.SIFT_create(10000)

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img_jigsaw, None)
kp2, des2 = sift.detectAndCompute(img_piece, None)

print("Detected keypoint features")

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=100)
search_params = dict(checks=500)   # or pass empty dictionary

flann = cv.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1, des2, k=2)

print("Ran FLANN matcher")

# Need to draw only good matches, so create a mask
matchesMask = [[0, 0] for i in range(len(matches))]

# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    if m.distance < 0.6 * n.distance:
        matchesMask[i] = [1, 0]

draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(255, 0, 0),
                   matchesMask=matchesMask,
                   flags=cv.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

img3 = cv.drawMatchesKnn(img_jigsaw, kp1, img_piece, kp2, matches, None, **draw_params)


# # RESIZE & SHOW RESULTS
width = int(1400)
height = int(1000)
dim = (width, height)
resized = cv.resize(img3, dim, interpolation=cv.INTER_AREA)

cv.imshow('sift_keypoints.jpg', resized)
cv.waitKey(0)
