import secrets
import cv2
import numpy as np
from map import Map, City, MapObject, Nation
import utils
import video_editing as ve
from video_editing import VideoMaker, VideoSection

from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip

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
        "Isfahan": City(3713, 2544, "Isfahan", img_file_path="images/assets/qwe.png"),
        "Mecca": City(3191, 3186, "Mecca", img_file_path="images/assets/qwe.png"),
        "Medina": City(3176, 3028, "Medina", img_file_path="images/assets/qwe.png")
    }
    for city_name, city in cities.items():
        map.add_object(city, is_static=True)
    print("Cities succesfully added")
    
    # Nations mask
    nations = [
        Nation("Fatmid Caliphate", (14, 127, 0, 255), font_bgra=(14, 87, 0, 255), capital=cities["Cairo"]),
        Nation("Seljuk Empire", (255, 148, 0, 255), font_bgra=(200, 128, 0, 255), capital=cities["Isfahan"]),
    ]
    nations_mask = cv2.imread("history/testYear.png", flags=cv2.IMREAD_UNCHANGED)
    map.set_nations_overlay(nations_mask, nations)
    print("Nations succesfully added")
    
    ## Video writer init
    out_video_path = "video.avi" if HIGH_QUALITY else "video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"MPEG") if HIGH_QUALITY else cv2.VideoWriter_fourcc(*"mp4v")

    video = VideoMaker(out_video_path, fourcc, Video.fps, (Video.width, Video.height), (Camera.width, Camera.height), verbose=1)

    clips = []
    total_fps = 5

    clip = ImageClip(map.get_map_img(0), duration=5)

    if (HIGH_QUALITY):
        clip.write_videofile("video.avi", fps=Video.fps, codec='rawvideo')
    else:
        clip.write_videofile("video.mp4", fps=Video.fps, threads=4)