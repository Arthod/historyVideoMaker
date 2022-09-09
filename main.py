import cv2
import numpy as np

width, height = 1920, 1080
fps = 60

def crop_image(img: np.array, x1: int, y1: int, width: int, height: int) -> np.array:
    return img[y1:y1 + height:1, x1:x1 + width:1]

img = cv2.imread("rivers.png").astype("uint8")


video = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
#video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*"MJPG"), fps, (width, height))

for i in range(10 * fps):
    img2 = crop_image(img, i, 0, width, height)

    video.write(img2)

video.release()

print("Rendering complete")