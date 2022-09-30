import sys
import numpy as np
import cv2
import utils

from map import Map

from config import Config as CF


def crop_image(img: np.array, x: int, y: int, width: int, height: int) -> np.array:
    return img[y:y + height, x:x + width]

def center_on_image(img: np.array, x: int, y: int, zoom: float, width, height):
    x_margin = round(width/2 * zoom)
    x = round(max(min(x, img.shape[1] - x_margin), x_margin))

    y_margin = round(height/2 * zoom)
    y = round(max(min(y, img.shape[0] - y_margin), y_margin))

    width = round(width * zoom)
    height = round(height * zoom)

    img = crop_image(img, x - width//2, y - height//2, width, height)
    return img

def play_video(video_path):
    
    # Play video
    cap = cv2.VideoCapture(video_path)
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
 

class Section:
    def __init__(self, frames_count: int, img: np.array):
        self.frames_count = frames_count


class MapVideo(Section):
    def __init__(self, frames_count: int, map: Map, zooms, xs, ys):
        self.frames_count = frames_count

        self.map = map
        self.zooms = zooms
        self.xs = xs
        self.ys = ys

    def next_img(self, frame: int):
        return self.map.get_map_img(frame)

class MapTransition(Section):
    def __init__(self, frames_count: int, map_img_old: np.array, map_img_new: np.array, zooms, xs, ys):
        self.frames_count = frames_count

        self.map_img_transition = utils.lerps_img_transition(map_img_old, map_img_new, frames_count)
        self.zooms = zooms
        self.xs = xs
        self.ys = ys

    def next_img(self, frame: int):
        return next(self.map_img_transition)


class VideoMaker(cv2.VideoWriter):
    def __init__(self, out_path, fourcc, fps, video_size, camera_size, verbose=0):
        super().__init__(out_path, fourcc, fps, video_size)
        self.video_width, self.video_height = video_size
        self.camera_width, self.camera_height = camera_size
        self.verbose = verbose

    def render_section(self, section: Section):
        frames_count = section.frames_count
        zooms = section.zooms
        xs = section.xs
        ys = section.ys

        if (not CF.IS_STILL_FRAMES):
            map_img = section.next_img(0)

        for frame in range(frames_count):
            if (CF.IS_STILL_FRAMES):
                map_img = section.next_img(frame)

            img_final = center_on_image(map_img, xs[frame], ys[frame], zooms[frame] * CF.IMG_SCALE, self.camera_width, self.camera_height)

            shape = img_final.shape
            if (shape[0] != self.video_height or shape[1] != self.video_width):
                if (shape[0] < self.video_height): # We need to enlargen the image
                    img_final = cv2.resize(img_final, (self.video_width, self.video_height), interpolation=cv2.INTER_CUBIC)
                else: # We need to shrink the image
                    img_final = cv2.resize(img_final, (self.video_width, self.video_height), interpolation=cv2.INTER_AREA)

            self.write(img_final.astype("uint8"))

            if (self.verbose >= 1):
                sys.stdout.write(f"\rFrame {frame + 1} / {frames_count}")
                sys.stdout.flush()
        print()