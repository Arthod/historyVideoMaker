import secrets
import cv2
import numpy as np
from map import Map, City, MapObject
import utils
import video_editing as ve
from video_editing import VideoMaker, VideoSection

DEBUG_MODE = True
HIGH_QUALITY = False

class Video:
    width = 1920
    height = 1080
    fps = 60

class Camera:
    width = 1920
    height = 1080


if __name__ == "__main__":
    ## Cities
    cities = {
        "Mecca": City(3206, 3178, "Mecca", img_file_path="images/assets/qwe.png"),
        "Medina": City(3832, 3025, "Medina", img_file_path="images/assets/qwe.png")
    }
    
    ## Map init
    map = Map()
    map.set_ck3_map()
    for city_name, city in cities.items():
        map.add_object(city, is_static=True)
    map.initialize()
    print("Map creation completed")

    ## Video writer init
    out_video_path = "video.avi" if HIGH_QUALITY else "video.mp4"
    if (HIGH_QUALITY):
        video = VideoMaker("video.mp4", cv2.VideoWriter_fourcc(*"MPEG"), Video.fps, (Video.width, Video.height), (Camera.width, Camera.height))
    else:
        video = VideoMaker(out_video_path, cv2.VideoWriter_fourcc(*"mp4v"), Video.fps, (Video.width, Video.height), (Camera.width, Camera.height))


    # Nations mask
    

    # Video sections
    sections = []

    fps_total = 5 * Video.fps
    mecca = cities["Mecca"]
    medina = cities["Medina"]
    sections.append(
        VideoSection(
            frames_count = fps_total,
            zooms = [1] * fps_total,
            xs = utils.lerps_expoential(mecca.x, medina.x, fps_total),
            ys = utils.lerps_expoential(mecca.y, medina.y, fps_total)
            )
    )

    # Video render & release
    video.render(sections, map, verbose=1)
    video.release()

    print("Rendering complete")

    #ve.play_video(out_video_path)