import cv2
import imutils
import numpy as np
from PIL import Image


def resize(image, size):
    print(f'Resizing image to:{size}')
    resized_image = image.resize(size)
    return resized_image


def cut_image_to_grid(pil_image):
    img = convert_to_cv_img(pil_image)
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

    return convert_to_pil_img(img)


def scale_contour(cnt, scale):
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    cnt_norm = cnt - [cx, cy]
    cnt_scaled = cnt_norm * scale
    cnt_scaled = cnt_scaled + [cx, cy]
    cnt_scaled = cnt_scaled.astype(np.int32)

    return cnt_scaled


def contour_crop(img, thresh=120, color=255):
    # convert the image to grayscale and threshold it
    gray = convert_to_cv_img(img, cv2.COLOR_BGR2GRAY)
    img = convert_to_cv_img(img)
    thresh = cv2.threshold(gray, thresh, color, cv2.THRESH_BINARY_INV)[1]

    #  find the largest contour in the threshold image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    color_mask = (color, color, color)

    # Extract image inside c
    output = img.copy()
    mask = np.zeros_like(output)  # Create mask where white is what we want, black otherwise
    cv2.drawContours(mask, [c], -1, color_mask, -1)  # Draw filled contour in mask
    out = np.zeros_like(output)  # Extract out the object and place into output image
    out[mask == color_mask] = output[mask == color_mask]

    # Crop image to contour area
    (y, x, z) = np.where(mask == color_mask)
    (topy, topx) = (np.min(y), np.min(x))
    (bottomy, bottomx) = (np.max(y), np.max(x))
    out = out[topy:bottomy + 1, topx:bottomx + 1]

    return convert_to_pil_img(out)


def draw_params(matches_mask=None):
    return dict(  # matchColor=(0, 0, 255),  # draw matches in blue
        # singlePointColor=(255, 0, 0),
        matchesThickness=10,
        matchesMask=matches_mask,  # draw only inliers
        flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)


def draw_params_SIFT(matches_mask=None):
    return dict(
        matchColor=(0, 0, 255),  # draw matches in blue
        singlePointColor=(255, 0, 0),
        matchesMask=matches_mask,  # draw only inliers
        flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)


def run_ORB_search(j_img, p_img):
    # Initiate SIFT detector
    orb = cv2.ORB_create(nfeatures=1000000, scoreType=cv2.ORB_HARRIS_SCORE)

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
    img = cv2.drawMatches(j_img, kp1, p_img, kp2, matches[:10], None, **draw_params())
    return convert_to_pil_img(img)


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
        if m.distance < 0.6 * n.distance:
            matches_mask[i] = [1, 0]

    img = cv2.drawMatchesKnn(j_img, kp1, p_img, kp2, matches, None, **draw_params_SIFT(matches_mask))
    return convert_to_pil_img(img)


def convert_to_cv_img(pil_img, mode=cv2.COLOR_RGB2BGR):
    cv_img = cv2.cvtColor(np.array(pil_img), mode)
    return cv_img


def convert_to_pil_img(cv_img, mode=cv2.COLOR_BGR2RGB):
    # OpenCV uses BGR and PIL uses RGB, flip from BGR to RGB before converting to PIL Image
    cv_rgb = cv2.cvtColor(cv_img, mode)
    pil_img = Image.fromarray(cv_rgb)

    return pil_img


def load_img_from_input(key, values):
    values = {k: v for k, v in values.items() if v}
    infile = values.get(key)
    if infile is None:
        raise Exception('Input file is empty.')

    return Image.open(infile)
