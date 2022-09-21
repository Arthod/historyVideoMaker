class Config:
    DEBUG_MODE = True
    HIGH_QUALITY = False

    OUT_VIDEO_PATH = "video.avi" if HIGH_QUALITY else "video.mp4"
    OUT_VIDEO_FOURCC = "MPEG" if HIGH_QUALITY else "mp4v"

    IMG_PATH = "metadata/interesting2.png" # metadata/interesting.png

    IMG_SCALE = 1

    CAMERA_WIDTH = 1920
    CAMERA_HEIGHT = 1080

    VIDEO_WIDTH = 1920
    VIDEO_HEIGHT = 1080
    VIDEO_FPS = 60

    NATION_DRAW_NAMES = True
    NATION_DRAW_OVERLAY = True

    CITY_DRAW_NAMES = True
    CITY_DRAW_SPRITE = True
    CITY_NAME_FONT_SIZE = 20 * IMG_SCALE
    CITY_NAME_FONT_PATH = "fonts/IMFeGPsc29P.ttf"
    CITY_NAME_Y_OFFSET = 24