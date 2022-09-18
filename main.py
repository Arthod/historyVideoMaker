import cv2
import numpy as np
from map import Map, City, MapObject
import utils
import video_editing as ve
from video_editing import VideoSection

DEBUG_MODE = True
HIGH_QUALITY = True

class Video:
    width = 1920
    height = 1080
    fps = 60

class Camera:
    width = 1920
    height = 1080


if __name__ == "__main__":
    ## Map init
    map = Map()
    map.set_ck3_map()
    map.add_object(City(3206, 3178, "Mecca", img_file_path="images/assets/qwe.png"), is_static=True)
    map.add_object(City(3832, 3025, "Medina", img_file_path="images/assets/qwe.png"), is_static=True)
    map.initialize()
    print("Map creation completed")

    ## Video writer init
    out_video_path = "video.avi" if HIGH_QUALITY else "video.mp4"
    if (HIGH_QUALITY):
        video = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*"MPEG"), Video.fps, (Video.width, Video.height))
    else:
        video = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*"mp4v"), Video.fps, (Video.width, Video.height))


    # Video sections
    fps_total = 5 * Video.fps
    sections = [
        VideoSection(
            frames_count = fps_total,
            zooms = [1] * fps_total,
            xs = utils.lerps_linear(1234, 3158, fps_total),
            ys = utils.lerps_linear(1109, 3791, fps_total)
            )
    ]

    
    for section in sections:
        frames_count = section.frames_count
        zooms = section.zooms
        xs = section.xs
        ys = section.ys

        for frame in range(frames_count):
            img_map = map.get_map_img(frame)
            img_final = ve.center_on_image(img_map, xs[frame], ys[frame], zooms[frame], Camera.width, Camera.height)

            shape = img_final.shape
            if (shape[0] != Video.height or shape[1] != Video.width):
                print("reshaping")
                img_final = cv2.resize(img_final, (Video.width, Video.height), interpolation=cv2.INTER_AREA)

            video.write(img_final.astype("uint8"))

    video.release()

    print("Rendering complete")

    ve.play_video(out_video_path)