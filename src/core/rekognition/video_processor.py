import cv2


def convert_vid_to_imgs(video, frame_rate, output_dir):
    """Given a video convert it to images and save to output_dir. 

    Note: The output images are used for training ML models.

    Args:
        video ([str]): Input video path.
        frame_rate ([int]): Number of images/frames to output
        output_dir ([str]): Directory to output frames to.
    """

    vidcap = cv2.VideoCapture(video)

    def writeImg(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        hasFrames, image = vidcap.read()
        if hasFrames:
            file_path = output_dir + "image" + str(count) + ".jpg"
            cv2.imwrite(file_path, image)  # save frame as JPG file

            print("Wrote image to path: " + file_path)
        return hasFrames
    sec = 0

    count = 1
    success = writeImg(sec)
    while success:
        count = count + 1
        sec = sec + frame_rate
        sec = round(sec, 2)
        success = writeImg(sec)


def main():
    print("Splitting Jigsaw video into images.")

    video = "jigsaw_examples/1000_tropics_jigsaw/jigsaw_video.mov"
    output_dir = "jigsaw_examples/1000_tropics_jigsaw/ml_dataset/"

    frame_rate = 1 / 60  # 60 images per second

    convert_vid_to_imgs(video, frame_rate, output_dir)


if __name__ == "__main__":
    main()
