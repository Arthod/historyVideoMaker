import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

from config import Config as CF

def lerps_linear(val_start: float, val_stop: float, count: int) -> list[float]:
    b = val_start
    a = (val_stop - b) / (count - 1)
    
    return [a * i + b for i in range(count)]

def lerps_exponential(val_start: float, val_stop: float, count: int) -> list[float]:
    b = pow(val_stop / val_start, 1 / (count - 1))
    a = val_start
    return [a * pow(b, i) for i in range(count)]

def lerps_img_transition(img_prev: np.array, img_next: np.array, count: int):
    for i in range(count):
        alpha = i / (count - 1)
        img = img_prev * (1 - alpha) + img_next * alpha
        yield img

def overlay_rgb_mask(img_curr, img_path, color_rgb):
    mask_new = cv2.imread(img_path, flags=cv2.IMREAD_GRAYSCALE)
    #mask_new = np.minimum(mask_new.astype("uint32") * 2, 255).astype("uint8")
    return np.minimum(np.stack((
        mask_new/255 * color_rgb[2] + img_curr[:,:, 0],
        mask_new/255 * color_rgb[1] + img_curr[:,:, 1],
        mask_new/255 * color_rgb[0] + img_curr[:,:, 2]
    ), axis=2), 255).astype("uint8")

def add_foreground_image(img_curr, img_ontop, alpha=1):
    alpha_foreground = (img_ontop[:,:,3] / 255.0) * alpha
    alpha_foreground_inv = (1 - alpha_foreground)

    for color in range(0, 3):
        img_curr[:,:,color] = img_ontop[:,:,color] * alpha_foreground + img_curr[:,:,color] * alpha_foreground_inv

    return img_curr

    return cv2.addWeighted(img_curr, alpha, img_ontop[...,0:3], 0.5, 0)

def rotate_image(image, angle):
    h, w = image.shape[:2]
    c_x, c_y = w//2, h//2

    M = cv2.getRotationMatrix2D((c_x, c_y), angle, 1)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated

def add_text(map_img, text, pos, font_size, color, shadow_offset, angle):
    font = ImageFont.truetype(CF.CITY_NAME_FONT_PATH, font_size)
    draw = ImageDraw.Draw(Image.fromarray(np.zeros((1, 1))))
    w, h = draw.textsize(text, font=font)

    size = max(w, h)
    text_img = np.zeros((size + shadow_offset[1] * 2, size + shadow_offset[0] * 2, 4)).astype("uint8")
    img_pil = Image.fromarray(text_img)
    draw = ImageDraw.Draw(img_pil)

    # Thin border
    x = shadow_offset[0]
    y = shadow_offset[1] + ((size - h) // 2)
    draw.text((x - shadow_offset[0], y), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x + shadow_offset[0], y), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x, y - shadow_offset[1]), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x, y + shadow_offset[1]), text, font=font, fill=(0, 0, 0, 255), align="center")

    # Thick border
    draw.text((x - shadow_offset[0], y - shadow_offset[1]), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x + shadow_offset[0], y - shadow_offset[1]), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x - shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=(0, 0, 0, 255), align="center")

    draw.text((x, y), text, font=font, fill=color, align="center")

    x = int(pos[0] - size / 2)
    y = int(pos[1] - size / 2)
    text_img = rotate_image(np.array(img_pil), angle)
    
    #text_img = cv2.cvtColor(text_img, cv2.COLOR_BGR2BGRA)
    map_img[y:y + text_img.shape[0], x:x + text_img.shape[1]] = add_foreground_image(map_img[y:y + text_img.shape[0], x:x + text_img.shape[1]], text_img)

    return map_img