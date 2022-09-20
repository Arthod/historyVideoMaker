import secrets
import cv2
import numpy as np
from map import Map, City, Nation
import utils
import video_editing as ve
from video_editing import MapTransition, MapVideo, VideoMaker

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
    width = 1920
    height = 1080
    fps = 60


if __name__ == "__main__":
    ## Map init
    map_terrain = Map(path="metadata/map_terrain.png")
    map_sepia = Map(path="metadata/map_sepia.png")
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
        Nation("Abbasid Caliphate", (0, 127, 38, 255), capital=cities["Baghdad"]),
        Nation("Qarmatians", (255, 255, 0, 255), capital=cities["Al-Hasa"]),
        Nation("Byzantine Empire", (55, 0, 127, 255), capital=cities["Constantinople"]),
        Nation("Saffarids", (59, 201, 211, 255), capital=cities["Shiraz"]),
        Nation("Samanid Empire", (71, 140, 211, 255), capital=cities["Bukhara"]),
    ]
    year927_mask = cv2.imread("history/927.png", flags=cv2.IMREAD_UNCHANGED)
    map_sepia.set_nations_overlay(year927_mask, nations)
    map_terrain.set_nations_overlay(year927_mask, nations)
    print("Nations succesfully added")


    # Initialize maps
    map_sepia.update_static(display_nation_names=True)
    map_terrain.update_static(display_nation_names=False)
    print("Static maps succesfully updated")

    
    ## Video writer init
    out_video_path = "video.avi" if HIGH_QUALITY else "video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"MPEG") if HIGH_QUALITY else cv2.VideoWriter_fourcc(*"mp4v")

    video = VideoMaker(out_video_path, fourcc, Video.fps, (Video.width, Video.height), (Camera.width, Camera.height), verbose=1)


    # Video render sections & release
    sections = []

    fps_total = 5 * Video.fps
    city1 = cities["Mecca"]
    city2 = cities["Isfahan"]
    video.render_section(
        MapVideo(
            frames_count = fps_total,
            map = map_sepia,
            zooms = [4] * fps_total,
            xs = utils.lerps_exponential(city1.x, city2.x, fps_total),
            ys = utils.lerps_exponential(city1.y, city2.y, fps_total)
            )
    )

    fps_total = 5 * Video.fps
    map_img_old = map_sepia.get_map_img(0)
    map_img_new = map_terrain.get_map_img(0)

    video.render_section(
        MapTransition(
            frames_count = fps_total,
            map_img_old = map_img_old,
            map_img_new = map_img_new,
            zooms = utils.lerps_exponential(4, 1, fps_total),
            xs = [city2.x] * fps_total,
            ys = [city2.y] * fps_total
        )
    )

    fps_total = 5 * Video.fps
    video.render_section(
        MapVideo(
            frames_count = fps_total,
            map = map_terrain,
            zooms = [1] * fps_total,
            xs = [city2.x] * fps_total,
            ys = [city2.y] * fps_total
        )
    )

    video.release()

    print("Rendering complete")

    ve.play_video(out_video_path)