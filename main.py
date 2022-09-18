import secrets
import cv2
import numpy as np
from map import Map, City, MapObject, Nation
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

class Video:
    width = 1280
    height = 768
    fps = 60


if __name__ == "__main__":
    ## Map init
    map = Map()
    map.set_ck3_map()
    print("Base map created")

    ## Cities
    cities = {
        "Cairo": City(2751, 2822, "Cairo", img_file_path="images/assets/qwe.png"),
        "Mecca": City(3206, 3178, "Mecca", img_file_path="images/assets/qwe.png"),
        "Mecca": City(3206, 3178, "Mecca", img_file_path="images/assets/qwe.png"),
        "Medina": City(3832, 3025, "Medina", img_file_path="images/assets/qwe.png")
    }
    for city_name, city in cities.items():
        map.add_object(city, is_static=True)
    print("Cities succesfully added")
    
    # Nations mask
    nations = [
        Nation("Fatmid Caliphate", (14, 127, 0, 255), (14, 87, 0, 255)),
        Nation("Seljuk Empire", (255, 148, 0, 255), (200, 128, 0, 255)),
    ]
    nations_mask = cv2.imread("history/testYear.png", flags=cv2.IMREAD_UNCHANGED)
    map.set_nations_overlay(nations_mask, nations)
    print("Nations succesfully added")

    map.update_static(display_nation_names=True)
    
    ## Video writer init
    out_video_path = "video.avi" if HIGH_QUALITY else "video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"MPEG") if HIGH_QUALITY else cv2.VideoWriter_fourcc(*"mp4v")

    video = VideoMaker(out_video_path, fourcc, Video.fps, (Video.width, Video.height), (Camera.width, Camera.height))


    # Video render sections & release
    sections = []

    fps_total = 5 * Video.fps
    mecca = cities["Mecca"]
    medina = cities["Medina"]
    video.render_section(
        VideoSection(
            map = map,
            frames_count = fps_total,
            zooms = [2] * fps_total,
            xs = utils.lerps_exponential(mecca.x, medina.x, fps_total),
            ys = utils.lerps_exponential(mecca.y, medina.y, fps_total)
            )
    )
    video.release()

    print("Rendering complete")

    ve.play_video(out_video_path)