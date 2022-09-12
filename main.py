import cv2
import numpy as np
from map import Map

class Video:
    width = 1920
    height = 1080
    fps = 60

class VideoTest:
    width = 1280
    height = 720
    fps = 60

def lerps_linear(val_start: float, val_stop: float, count: int) -> list[float]:
    b = val_start
    a = (val_stop - b) / (count - 1)
    
    return [a * i + b for i in range(count)]

def lerps_expoential(val_start: float, val_stop: float, count: int) -> list[float]:
    b = pow(val_stop / val_start, 1 / (count - 1))
    a = val_start
    return [a * pow(b, i) for i in range(count)]

def crop_image(img: np.array, x: int, y: int, width: int, height: int) -> np.array:
    return img[y:y + height, x:x + width]

def center_on_image(img: np.array, x: int, y: int, zoom: float):
    x_margin = round(Video.width/2 * zoom)
    x = round(max(min(x, img.shape[1] - x_margin), x_margin))

    y_margin = round(Video.height/2 * zoom)
    y = round(max(min(y, img.shape[0] - y_margin), y_margin))

    width = round(Video.width * zoom)
    height = round(Video.height * zoom)

    img = crop_image(img, x - width//2, y - height//2, width, height)
    return img

if __name__ == "__main__":

    img = Map.get_ck3_map()
    print("Map creation completed")


    video = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*"mp4v"), Video.fps, (Video.width, Video.height))
    #video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*"MJPG"), fps, (Video.width, Video.height))

    fps_total = 10 * Video.fps

    zoom_stages = [1] * fps_total
    xs = lerps_linear(3234, 3158, fps_total)
    ys = lerps_linear(3109, 2491, fps_total)
    for i in range(fps_total):
        img_final = center_on_image(img, xs[i], ys[i], zoom_stages[i])

        shape = img_final.shape
        if (shape[0] != Video.height or shape[1] != Video.width):
            img_final = cv2.resize(img_final, (Video.width, Video.height), interpolation=cv2.INTER_CUBIC)

        video.write(img_final)

    video.release()

    print("Rendering complete")