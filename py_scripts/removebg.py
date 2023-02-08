from PIL import Image 
import numpy as np

# thresh = 250
thresh = 240

def make_transparent(img):
    img = img.convert('RGBA')
    datas = img.getdata()
    newData = []

    for items in datas:
        if items[0] >= thresh and items[1] >= thresh and items[2] >= thresh:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(items)
    img.putdata(newData)
    return img


def removebg_fn(full_filename):
    full_filename_output  = full_filename.replace('.png', '_output.png')
    img = Image.open(full_filename)
    img = img.convert('RGBA')
    data = np.array(img)
    red, blue, green, alpha = data.T

    red_areas = red >= thresh
    green_areas = green >= thresh
    blue_areas = blue >= thresh

    data[..., :-1][red_areas.T] = (255, 255, 255)
    data[..., :-1][green_areas.T] = (255, 255, 255)
    data[..., :-1][blue_areas.T] = (255, 255, 255)

    img2 = Image.fromarray(data)
    # make image transparent
    img2 = make_transparent(img2)
    img2.save(full_filename_output)
    return full_filename_output
