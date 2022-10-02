import secrets
import cv2
import numpy as np
from map import Map, City, Nation
import utils
import video_editing as ve
from video_editing import Section, VideoMaker

from config import Config as CF

if __name__ == "__main__":
    ## Map init
    map = Map(path=f"{CF.IMG_MAIN_PATH}")
    print("Base map created")

    ## Cities
    cities = {
        # https://www.worldhistory.org/uploads/images/15330.png?v=1647975399
        # https://upload.wikimedia.org/wikipedia/commons/a/ad/Abbasid_Caliphate_891-892.png
        # Egypt and Levantine
        "Cairo": City(2751, 2822, "Cairo"),
        "Alexandria": City(2697, 2770, "Alexandria"),
        "Gaza": City(2915, 2735, "Gaza"),
        "Antioch": City(2997, 2435, "Antioch"),
        "Edessa": City(3111, 2351, "Edessa"),
        "Aleppo": City(3032, 2416, "Aleppo"),
        "Damascus": City(3026, 2602, "Damascus"),
        "Jerusalem": City(2965, 2634, "Jerusalem"),
        "Barca": City(2221, 2750, "Barca"),
        "Damietta": City(2772, 2763, "Damietta"),
        "Faiyum": City(2728, 2856, "Faiyum"),
        "El-Ashmunein": City(2732, 2933, "El-Ashmunein"),
        "Asyut": City(2743, 2963, "Asyut"),
        "Akhmim": City(2783, 2984, "Akhmim"),
        "Qus": City(2829, 3018, "Qus"),
        "Aswan": City(2840, 3108, "Aswan"),
        "Aqaba": City(2945, 2814, "Aqaba"),
        "Tiberias": City(2968, 2648, "Tiberias"),
        "Manbij": City(3077, 2410, "Manbij"),
        "Tripoli": City(2981, 2558, "Tripoli"),
        "Tadmor": City(3089, 2569, "Tadmor"),
        "Raqqa": City(3138, 2445, "Raqqa"),

        
        # Arabia
        "Muscat": City(4085, 3001, "Al-Masqat"),
        "Bahrain": City(3962, 2906, "Bahrain"),
        "Daba": City(3972, 2908, "Daba"),
        "Suhar": City(3996, 2969, "Suhar"),
        "Hormuz": City(4005, 2829, "Damascus"),
        "Al-Hasa": City(3669, 2937, "Al-Hasa"),
        "Mecca": City(3191, 3186, "Mecca"),
        "Medina": City(3176, 3028, "Medina"),
        "Tabuk": City(3034, 2898, "Tabuk"),
        "Zabid": City(3347, 3384, "Zabid"),
        "Aden": City(3473, 3566, "Aden"),
        "Qatif": City(3659, 2881, "Qatif"),
        "Zubala": City(3366, 2811, "Zubala"),
        "Jiddah": City(3157, 3152, "Jiddah"),
        "Sana": City(3409, 3488, "Sana"),
        "Najran": City(3468, 3344, "Najran"),

        # Iraq
        "Kufa": City(3381, 2613, "Kufa"),
        "Basra": City(3550, 2690, "Basra"),
        "Baghdad": City(3394, 2541, "Baghdad"),
        "Mosul": City(3316, 2383, "Mosul"),
        "al-Qarqisiya": City(3188, 2469, "al-Qarqisiya"),
        "Haditha": City(3285, 2514, "Haditha"),
        "Anbar": City(3356, 2555, "Anbar"),
        "Kufa": City(3396, 2629, "Kufa"),
        "Abadan": City(3555, 2692, "Abadan"),
        "Ahvaz": City(3588, 2651, "Ahvaz"),
        "Samarra": City(3376, 2511, "Samarra"),
        "Tikrit": City(3352, 2489, "Tikrit"),
        "Hulwan": City(2456, 2462, "Hulwan"),



        # Persia
        "Jullafar": City(3946, 2905, "Jullafar"),
        "Jannaba": City(3680, 2711, "Jannaba"),
        "Arrajan": City(3678, 2672, "Arrajan"),
        "Fasa": City(3827, 2753, "Fasa"),
        "Hormuz": City(3976, 2821, "Hormuz"),
        "Jiruft": City(4019, 2769, "Jiruft"),
        "Tis": City(4072, 2894, "Tis"),
        "Siraf": City(3771, 2812, "Siraf"),
        "Bukhara": City(4255, 2114, "Bukhara"),
        "Shiraz": City(3791, 2744, "Shiraz"),
        "Isfahan": City(3713, 2544, "Isfahan"),
        "Amol": City(3749, 2314, "Amol"),
        "Gorgan": City(3836, 2285, "Gorgan"),
        "Damaghan": City(3833, 2343, "Damaghan"),
        "Ardabil": City(3554, 2242, "Ardabil"),
        "Baku": City(3588, 2093, "Baku"),
        "Maraghah": City(3439, 2270, "Maraghah"),
        "Bardha'ah": City(3460, 2086, "Bardha'ah"),
        "Zanjan": City(3569, 2329, "Zanjan"),
        "Qazwin": City(3633, 2339, "Qazwin"),
        "Hulwan": City(3452, 2468, "Hulwan"),
        "Dinawar": City(3528, 2451, "Dinawar"),
        "Qumm": City(3687, 2441, "Qumm"),
        "Sariyah": City(3781, 2308, "Sariyah"),
        "Rayy": City(3716, 2364, "Rayy"),
        "Jurjan": City(3901, 2267, "Jurjan"),
        "Nasa": City(4010, 2216, "Nasa"),
        "Darabjird": City(3882, 2753, "Darabjird"),
        "Sirjan": City(3939, 2733, "Sirjan"),
        "Bamm": City(4076, 2732, "Bamm"),
        "Fannazbur": City(4400, 2795, "Fannazbur"),
        "Zaranj": City(4175, 2576, "Zaranj"),
        "Bust": City(4333, 2549, "Bust"),
        "Yazd": City(3822, 2637, "Yazd"),

        # Anatolia
        "Ankara": City(2825, 2194, "Ankara"),
        "Nicea": City(2642, 2178, "Nicea"),
        "Abydos": City(2476, 2208, "Abydos"),
        "Smyrna": City(2518, 2334, "Smyrna"),
        "Nicosia": City(2856, 2514, "Nicosia"),
        "Tarsos": City(2916, 2396, "Tarsos"),
        "Antalya": City(2710, 2421, "Antalya"),
        "Ephesos": City(2529, 2370, "Ephesos"),
        "Sardis": City(2561, 2332, "Sardis"),
        "Sinop": City(2899, 2047, "Sinop"),
        "Trapezus": City(3134, 2099, "Trapezus"),
        "Konya": City(2808, 2353, "Konya"),
        "Van":  City(3311, 2232, "Van"),
        "Manzikert": City(3274, 2209, "Manzikert"),
        "Malatya": City(3090, 2270, "Malatya"),
        "Bitlis": City(3267, 2264, "Bitlis"),

        # Greece
        "Constantinople": City(2585, 2127, "Constantinople"),
        "Candia": City(2434, 2559, "Candia"),
        "Athens": City(2330, 2375, "Athens"),
        "Patra": City(2220, 2368, "Patra"),
        "Mistra": City(2241, 2445, "Mistra"),
        "Larissa": City(2272, 2267, "Larissa"),
        "Thessaloniki": City(2276, 2180, "Thessaloniki"),
        "Corinth": City(2292, 2389, "Corinth"),
        "Adrianople": City(2469, 2095, "Adrianople"),
        "Philippopolis": City(2362, 2062, "Philippopolis"),

        # Italy
        "Amalfi": City(1811, 2203, "Amalfi"),
        "Bari": City(1925, 2171, "Bari"),
        "Messina": City(1851, 2383, "Messina"),
    }
    for city_name, city in cities.items():
        map.add_object(city, is_static=True)
    print("Cities succesfully added")
    
    # Nations mask
    nations = [
        Nation("Byzantine Empire", (55, 0, 127, 255), cities["Constantinople"], (2600, 2220), 85, 5),
        Nation("Abbasid Caliphate", (0, 127, 38, 255), cities["Baghdad"], (3300, 2600), 70, 30),
        #Nation("Qarmatians", (255, 255, 0, 255), cities["Al-Hasa"], (3690, 2930), 50, -43),
        #Nation("Saffarids", (59, 201, 211, 255), cities["Shiraz"], (3870, 2720), 55, -20),
        #Nation("Samanid Empire", (71, 140, 211, 255), cities["Bukhara"], (4179, 2385), 80, 0),
        Nation("Oman", (213, 170, 128, 255), cities["Suhar"], (4073, 3072), 46, 300),
        Nation("Tulunids", (0, 127, 147, 255), cities["Cairo"], (2680, 2815), 80, 5),
    ]
    map.nations = nations
    print("Nations succesfully added")

    
    ## Video writer init
    out_video_path = CF.OUT_VIDEO_PATH
    fourcc = cv2.VideoWriter_fourcc(*CF.OUT_VIDEO_FOURCC)
    video = VideoMaker(out_video_path, fourcc, CF.VIDEO_FPS, (CF.VIDEO_WIDTH, CF.VIDEO_HEIGHT), (CF.CAMERA_WIDTH, CF.CAMERA_HEIGHT), verbose=1)

    # Video render sections & release
    sections = []

    city1 = cities["Mecca"]
    city2 = cities["Baghdad"]

    if (False):
        img = map_terrain.get_map_img(0)
        img = ve.center_on_image(img, city2.x, city2.y, 1, CF.CAMERA_WIDTH, CF.CAMERA_HEIGHT)
        shape = img.shape
        if (shape[0] != CF.VIDEO_HEIGHT or shape[1] != CF.VIDEO_WIDTH):
            if (shape[0] < CF.VIDEO_HEIGHT): # We need to enlargen the image
                img = cv2.resize(img, (CF.VIDEO_WIDTH, CF.VIDEO_HEIGHT), interpolation=cv2.INTER_CUBIC)
            else: # We need to shrink the image
                img = cv2.resize(img, (CF.VIDEO_WIDTH, CF.VIDEO_HEIGHT), interpolation=cv2.INTER_AREA)
                

        cv2.imshow("asd", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        Section.map = map

        fps_total = 1 * CF.VIDEO_FPS
        video.render_section(
            Section(
                frames_count = fps_total,
                zooms = [1] * fps_total,#utils.lerps_exponential(1, 2, int(fps_total // 2)) + utils.lerps_exponential(2, 1, int(fps_total // 2)),
                xs = utils.lerps_linear(city1.x, city2.x, fps_total),
                ys = utils.lerps_linear(city1.y, city2.y, fps_total),
                history_year = 900
            )
        )

        fps_total = 2 * CF.VIDEO_FPS
        video.render_section(
            Section(
                frames_count = fps_total,
                zooms = [1] * fps_total,
                xs = [city2.x] * fps_total,
                ys = [city2.y] * fps_total,
                history_year = 900,
                history_year_new = 901
            )
        )

        fps_total = 2 * CF.VIDEO_FPS
        video.render_section(
            Section(
                frames_count = fps_total,
                zooms = [1] * fps_total,
                xs = [city2.x] * fps_total,
                ys = [city2.y] * fps_total,
                history_year = 901,
            )
        )

        video.release()

        print("Rendering complete")

        ve.play_video(out_video_path)