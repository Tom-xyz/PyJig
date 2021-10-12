from PIL import Image
import numpy

import cv2


def resize(image, size):
    new_width, new_height = size
    resized_image = image.resize(size)
    print(f"The resized image size is {new_width}px wide x {new_height}px high")
    return resized_image


def cut_image_to_grid(pil_image):
    img = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
    image_copy = img.copy()
    imgheight = img.shape[0]
    imgwidth = img.shape[1]

    # TODO: HARDCODING CELL SIZE, REPLACE WITH DYNAMIC CELL SIZE
    M = 30
    N = 30
    x1 = 0
    y1 = 0

    for y in range(0, imgheight, M):
        for x in range(0, imgwidth, N):
            if (imgheight - y) < M or (imgwidth - x) < N:
                break

            y1 = y + M
            x1 = x + N

            # check whether the patch width or height exceeds the image width or height
            if x1 >= imgwidth and y1 >= imgheight:
                x1 = imgwidth - 1
                y1 = imgheight - 1
                # Crop into patches of size MxN
                tiles = image_copy[y:y + M, x:x + N]
                # Save each patch into file directory
                cv2.imwrite('saved_patches/' + 'tile' + str(x) + '_' + str(y) + '.jpg', tiles)
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)
            elif y1 >= imgheight:  # when patch height exceeds the image height
                y1 = imgheight - 1
                # Crop into patches of size MxN
                tiles = image_copy[y:y + M, x:x + N]
                # Save each patch into file directory
                cv2.imwrite('saved_patches/' + 'tile' + str(x) + '_' + str(y) + '.jpg', tiles)
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)
            elif x1 >= imgwidth:  # when patch width exceeds the image width
                x1 = imgwidth - 1
                # Crop into patches of size MxN
                tiles = image_copy[y:y + M, x:x + N]
                # Save each patch into file directory
                cv2.imwrite('saved_patches/' + 'tile' + str(x) + '_' + str(y) + '.jpg', tiles)
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)
            else:
                # Crop into patches of size MxN
                tiles = image_copy[y:y + M, x:x + N]
                # Save each patch into file directory
                cv2.imwrite('saved_patches/' + 'tile' + str(x) + '_' + str(y) + '.jpg', tiles)
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)

    # return cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    return Image.fromarray(img)
