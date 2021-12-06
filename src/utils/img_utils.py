import cv2
import numpy as np
from PIL import Image


def resize(image, size):
    print(f'Resizing image to:{size}')
    resized_image = image.resize(size)
    return resized_image


def cut_image_to_grid(pil_image):
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    img_height = img.shape[0]
    img_width = img.shape[1]

    # TODO: Use dynamic cell size
    M = 30
    N = 30

    for y in range(0, img_height, M):
        for x in range(0, img_width, N):
            if (img_height - y) < M or (img_width - x) < N:
                break

            y1 = y + M
            x1 = x + N

            # check whether the patch width or height exceeds the image width or height
            if x1 >= img_width and y1 >= img_height:
                x1 = img_width - 1
                y1 = img_height - 1
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)
            elif y1 >= img_height:  # when patch height exceeds the image height
                y1 = img_height - 1
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)
            elif x1 >= img_width:  # when patch width exceeds the image width
                x1 = img_width - 1
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)
            else:
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)

    return Image.fromarray(img)


def identify_contour(piece, threshold_low=99, threshold_high=255):
    """Identify the contour around the piece"""
    piece = cv2.cvtColor(piece, cv2.COLOR_BGR2GRAY)  # better in grayscale
    ret, thresh = cv2.threshold(piece, threshold_low, threshold_high, 0)
    contours, hiers = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_sorted = np.argsort(list(map(cv2.contourArea, contours)))
    return contours, contour_sorted[-2]


def get_bounding_rect(contour):
    """Return the bounding rectangle given a contour"""
    x, y, w, h = cv2.boundingRect(contour)
    return x, y, w, h


def draw_params(matches_mask=None):
    return dict(matchColor=(0, 0, 255),  # draw matches in blue
                singlePointColor=(255, 0, 0),
                matchesMask=matches_mask,  # draw only inliers
                flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)


def run_ORB_search(j_img, p_img):
    # Initiate SIFT detector
    orb = cv2.ORB_create(nfeatures=100000, scoreType=cv2.ORB_HARRIS_SCORE, edgeThreshold=20, scaleFactor=1.5)

    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(j_img, None)
    kp2, des2 = orb.detectAndCompute(p_img, None)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw first 10 matches.
    img = cv2.drawMatches(j_img, kp1, p_img, kp2, matches[:10], outImg=None, **draw_params())
    return Image.fromarray(img)


def run_SIFT_search(j_img, p_img):
    # Initiate SIFT detector
    sift = cv2.SIFT_create(10000)

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(j_img, None)
    kp2, des2 = sift.detectAndCompute(p_img, None)

    print("Detected keypoint features")

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=100)
    search_params = dict(checks=500)  # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    print("Ran FLANN matcher")

    # Need to draw only good matches, so create a mask
    matches_mask = [[0, 0] for i in range(len(matches))]

    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matches_mask[i] = [1, 0]

    img = cv2.drawMatchesKnn(j_img, kp1, p_img, kp2, matches, None, **draw_params(matches_mask))
    return Image.fromarray(img)
