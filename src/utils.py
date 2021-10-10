from PIL import Image

def resize(input_file, size):
    image = Image.open(input_file)
    width, height = image.size
    print(f"The original image size is {width}px wide x {height}px high")
    new_width, new_height = size
    scale = min(new_height / height, new_width / width)
    resized_image = image.resize(
        (int(width * scale), int(height * scale)), Image.ANTIALIAS)
    resized_image = image.resize(size)
    width, height = resized_image.size
    print(f"The resized image size is {width}px wide x {height}px high")
    return resized_image