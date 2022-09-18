import sys
import numpy as np
import cv2


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
 

class VideoSection:
    def __init__(self, frames_count, zooms, xs, ys):
        self.frames_count = frames_count
        self.zooms = zooms
        self.xs = xs
        self.ys = ys

        self._validate()


    def _validate(self):
        # Assert have same length
        assert self.frames_count == len(self.zooms)
        assert self.frames_count == len(self.xs)
        assert self.frames_count == len(self.ys)

class VideoMaker(cv2.VideoWriter):
    def __init__(self, out_path, fourcc, fps, video_size, camera_size):
        super().__init__(out_path, fourcc, fps, video_size)
        self.video_width, self.video_height = video_size
        self.camera_width, self.camera_height = camera_size

    def render(self, sections: list[VideoSection], map, verbose=0):
        for i, section in enumerate(sections):
            frames_count = section.frames_count
            zooms = section.zooms
            xs = section.xs
            ys = section.ys

            for frame in range(frames_count):
                img_map = map.get_map_img(frame)
                img_final = center_on_image(img_map, xs[frame], ys[frame], zooms[frame], self.camera_width, self.camera_height)

                shape = img_final.shape
                if (shape[0] != self.video_height or shape[1] != self.video_width):
                    print("reshaping")
                    img_final = cv2.resize(img_final, (self.video_width, self.video_height), interpolation=cv2.INTER_AREA)

                self.write(img_final.astype("uint8"))

                if (verbose >= 1):
                    sys.stdout.write(f"\rSection {i + 1} / {len(sections)}, Frame {frame + 1} / {frames_count}")
                    sys.stdout.flush()
        print()
