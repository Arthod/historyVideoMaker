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

    for color in range(0, 3):
        img_curr[:,:,color] = (alpha_foreground) * img_ontop[:,:,color] + img_curr[:,:,color] * (1 - alpha_foreground)

    return img_curr

def rotate_image(image, angle):
    h, w = image.shape[:2]
    c_x, c_y = w//2, h//2

    M = cv2.getRotationMatrix2D((c_x, c_y), angle, 1)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated

def add_text(map_img, text, pos, font_size, color, shadow_offset=None):
    if (shadow_offset is None):
        x_shadow_offset = 1
        y_shadow_offset = 1
    else:
        x_shadow_offset, y_shadow_offset = shadow_offset

    img_pil = Image.fromarray(map_img)
    draw = ImageDraw.Draw(img_pil)

    font = ImageFont.truetype(CF.CITY_NAME_FONT_PATH, font_size)

    w, h = draw.textsize(text, font=font)
    x, y = pos
    x = x - w / 2
    y = y - h / 2

    # Thin border
    draw.text((x - x_shadow_offset, y), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x + x_shadow_offset, y), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x, y - y_shadow_offset), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x, y + y_shadow_offset), text, font=font, fill=(0, 0, 0, 255), align="center")

    # Thick border
    draw.text((x - x_shadow_offset, y - y_shadow_offset), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x + x_shadow_offset, y - y_shadow_offset), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x - x_shadow_offset, y + y_shadow_offset), text, font=font, fill=(0, 0, 0, 255), align="center")
    draw.text((x + x_shadow_offset, y + y_shadow_offset), text, font=font, fill=(0, 0, 0, 255), align="center")

    draw.text((x, y), text, font=font, fill=color, align="center")
    map_img = np.array(img_pil)
    return map_img