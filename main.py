import secrets
import cv2
import numpy as np
from map import Map, City, Nation
import utils
import video_editing as ve
from video_editing import MapTransition, MapVideo, VideoMaker

from config import Config as CF

if __name__ == "__main__":
    ## Map init
    map_terrain = Map(path=CF.IMG_PATH)
    print("Base map created")

    ## Cities
    cities = {
        "Cairo": City(2751, 2822, "Cairo", img_file_path="images/assets/qwe.png"),
        "Isfahan": City(3713, 2544, "Isfahan", img_file_path="images/assets/qwe.png"),
        "Mecca": City(3191, 3186, "Mecca", img_file_path="images/assets/qwe.png"),
        "Medina": City(3176, 3028, "Medina", img_file_path="images/assets/qwe.png"),
        "Baghdad": City(3470, 2607, "Baghdad", img_file_path="images/assets/qwe.png"),
        "Basra": City(3550, 2690, "Basra", img_file_path="images/assets/qwe.png"),
        "Al-Hasa": City(3669, 2937, "Al-Hasa", img_file_path="images/assets/qwe.png"),
        "Constantinople": City(2585, 2127, "Constantinople", img_file_path="images/assets/qwe.png"),
        "Shiraz": City(3791, 2744, "Shiraz", img_file_path="images/assets/qwe.png"),
        "Bukhara": City(4255, 2114, "Bukhara", img_file_path="images/assets/qwe.png")
    }
    for city_name, city in cities.items():
        map_terrain.add_object(city, is_static=True)
    print("Cities succesfully added")
    
    # Nations mask
    nations = [
        Nation("Abbasid Caliphate", (0, 127, 38, 255), cities["Baghdad"], 
            (3050, 2677), 80, 25),
        Nation("Qarmatians", (255, 255, 0, 255), cities["Al-Hasa"],
            (3690, 2930), 50, -43),
        Nation("Byzantine Empire", (55, 0, 127, 255), cities["Constantinople"],
            (2850, 2240), 65, 18),
        Nation("Saffarids", (59, 201, 211, 255), cities["Shiraz"],
            (3870, 2720), 55, -20),
        Nation("Samanid Empire", (71, 140, 211, 255), cities["Bukhara"],
            (4179, 2385), 80, 0),
        Nation("Oman", (213, 170, 128, 255), cities["Bukhara"],
            (4053, 3072), 40, 300),
    ]
    year927_mask = cv2.imread("history/927.png", flags=cv2.IMREAD_UNCHANGED)
    map_terrain.set_nations_overlay(year927_mask, nations)
    print("Nations succesfully added")


    # Initialize maps
    map_terrain.update_static(display_nation_names=True)
    print("Static maps succesfully updated")

    
    ## Video writer init
    out_video_path = CF.OUT_VIDEO_PATH
    fourcc = cv2.VideoWriter_fourcc(*CF.OUT_VIDEO_FOURCC)
    video = VideoMaker(out_video_path, fourcc, CF.VIDEO_FPS, (CF.VIDEO_WIDTH, CF.VIDEO_HEIGHT), (CF.CAMERA_WIDTH, CF.CAMERA_HEIGHT), high_quality=CF.HIGH_QUALITY, verbose=1)


    # Video render sections & release
    sections = []

    city1 = cities["Constantinople"]
    city2 = cities["Mecca"]

    fps_total = 5 * CF.VIDEO_FPS
    video.render_section(
        MapVideo(
            frames_count = fps_total,
            map = map_terrain,
            zooms = [2] * fps_total,
            xs = [city2.x] * fps_total,
            ys = [city2.y] * fps_total
        )
    )
    """
    video.render_section(
        MapVideo(
            frames_count = fps_total,
            map = map_terrain,
            zooms = utils.lerps_exponential(1, 2, int(fps_total//2)) + utils.lerps_exponential(2, 1, int(fps_total//2)),
            xs = utils.lerps_linear(city1.x, city2.x, fps_total),
            ys = utils.lerps_linear(city1.y, city2.y, fps_total),
        )
    )

    fps_total = 5 * CF.VIDEO_FPS
    video.render_section(
        MapVideo(
            frames_count = fps_total,
            map = map_terrain,
            zooms = [1] * fps_total,
            xs = [city2.x] * fps_total,
            ys = [city2.y] * fps_total
        )
    )"""

    video.release()

    print("Rendering complete")

    ve.play_video(out_video_path)