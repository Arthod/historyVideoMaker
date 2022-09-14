import cv2
import numpy as np
from map import Map, City, MapObject

class Video:
    width = 1920
    height = 1080
    fps = 60

class Camera:
    width = 1920
    height = 1080

class Video:
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
    x_margin = round(Camera.width/2 * zoom)
    x = round(max(min(x, img.shape[1] - x_margin), x_margin))

    y_margin = round(Camera.height/2 * zoom)
    y = round(max(min(y, img.shape[0] - y_margin), y_margin))

    width = round(Camera.width * zoom)
    height = round(Camera.height * zoom)

    img = crop_image(img, x - width//2, y - height//2, width, height)
    return img

if __name__ == "__main__":
    map = Map()
    map.set_ck3_map()
    map.add_object(City(3206, 3178, "Mecca", img_file_path="images/assets/qwe.png"), is_static=True)
    map.add_object(City(3154, 3025, "Medina", img_file_path="images/assets/qwe.png"), is_static=True)
    print("Map creation completed")


    video = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*"mp4v"), Video.fps, (Video.width, Video.height))
    #video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*"MJPG"), fps, (Video.width, Video.height))

    fps_total = 5 * Video.fps

    zoom_stages = [1] * fps_total
    xs = lerps_linear(3234, 3158, fps_total)
    ys = lerps_linear(3109, 2791, fps_total)
    for frame in range(fps_total):
        img_map = map.get_map_img(frame)
        img_final = center_on_image(img_map, xs[frame], ys[frame], zoom_stages[frame])

        shape = img_final.shape
        if (shape[0] != Video.height or shape[1] != Video.width):
            img_final = cv2.resize(img_final, (Video.width, Video.height), interpolation=cv2.INTER_AREA)

        video.write(img_final.astype("uint8"))

    video.release()

    print("Rendering complete")


    # Play video
    cap = cv2.VideoCapture("video.mp4")
    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video file")
    
    # Read until video is completed
    while(cap.isOpened()):
        
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
        # Display the resulting frame
            cv2.imshow('Frame', frame)
            
        # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    
    # Break the loop
        else:
            break
 