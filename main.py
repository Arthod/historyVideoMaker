import cv2
import numpy as np

width, height = 1920, 1080
fps = 60

def lerps_linear(val_start: float, val_stop: float, count: int) -> list[float]:
    b = val_start
    a = (val_stop - b) / (count - 1)
    
    return [a * i + b for i in range(count)]

def crop_image(img: np.array, x: int, y: int, width: int, height: int) -> np.array:
    return img[y:y + height, x:x + width]

def center_on_image(img: np.array, x: int, y: int, zoom: float):
    x_margin = int(width/2 * zoom)
    x = max(min(x, img.shape[1] - x_margin), x_margin)

    y_margin = int(height/2 * zoom)
    y = max(min(y, img.shape[0] - y_margin), y_margin)

    w = int(width * zoom)
    h = int(height * zoom)

    img = crop_image(img, x - w//2, y - h//2, w, h)
    return img

if __name__ == "__main__":

    img = cv2.imread("images/map/rivers.png").astype("uint8")


    video = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    #video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*"MJPG"), fps, (width, height))

    zoom_stages = lerps_linear(1, 0.1, 5 * fps) + [0.1] * 5 * fps
    x = 1567
    y = 1037
    for i in range(10 * fps):
        img_final = center_on_image(img, x, y, zoom_stages[i])

        shape = img_final.shape
        if (shape[0] != height or shape[1] != width):
            img_final = cv2.resize(img_final, (width, height), interpolation=cv2.INTER_CUBIC)

        video.write(img_final)

    video.release()

    print("Rendering complete")