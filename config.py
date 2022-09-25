class Config:
    DEBUG_MODE = True
    HIGH_QUALITY = True
    IS_STILL_FRAMES = HIGH_QUALITY # Whether map_get_img should get next frame during render_section
    IS_FULL_HD = HIGH_QUALITY # If it is FULL HD
    IS_BIG_MAP = HIGH_QUALITY
    IS_GOOD_FOURCC = False


    OUT_VIDEO_PATH = "video.avi" if IS_GOOD_FOURCC else "video.mp4"
    OUT_VIDEO_FOURCC = "MPEG" if IS_GOOD_FOURCC else "mp4v"

    IMG_BIG_OR_SMALL = "big" if IS_BIG_MAP else "small"
    IMG_HISTORY_PATH = f"history/{IMG_BIG_OR_SMALL}"
    IMG_MAIN_PATH = f"metadata/{IMG_BIG_OR_SMALL}/map.png"

    IMG_SCALE = 4 if IS_BIG_MAP else 1

    CAMERA_WIDTH = 1920
    CAMERA_HEIGHT = 1080

    VIDEO_WIDTH = 1920 if IS_FULL_HD else 1280
    VIDEO_HEIGHT = 1080 if IS_FULL_HD else 720
    VIDEO_FPS = 60 if IS_FULL_HD else 30

    NATION_DRAW_NAMES = True
    NATION_DRAW_OVERLAY = True

    CITY_DRAW_NAMES = True
    CITY_DRAW_SPRITE = True
    CITY_NAME_FONT_SIZE = 20 * IMG_SCALE
    CITY_NAME_FONT_PATH = "fonts/IMFeGPsc29P.ttf"
    CITY_NAME_Y_OFFSET = 24