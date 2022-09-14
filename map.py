# Combine images to form a map (3d map?)

import random
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np

class Map:
    def __init__(self):
        self.map_img = None
        self.static_objects: list[MapObject] = []
        self.dynamic_objects: list[MapObject] = []

    @staticmethod
    def _overlay_rgb_mask(img_curr, mask_new, color_bgr):
        img_new = np.stack((
            np.round(mask_new/255 * color_bgr[0]),# + (1 - mask_curr/255) * img_curr[...,0]/255),
            np.round(mask_new/255 * color_bgr[1]),# + (1 - mask_curr/255) * img_curr[...,1]/255),
            np.round(mask_new/255 * color_bgr[2])# + (1 - mask_curr/255) * img_curr[...,2]/255)
            ), axis=2).astype("uint8")
        #img_curr = np.multiply(img/255, mask_new/255) + np.multiply(img_curr, (1 - mask_curr/255))
        img_curr = cv2.addWeighted(img_curr, 1, img_new, 1, 0)# = mask_curr + mask_new#np.minimum(mask_curr + mask_new, 255)

        return img_curr

    @staticmethod
    def _add_foreground_image(img_curr, img_ontop):
        alpha_foreground = img_ontop[:,:,3] / 255.0

        for color in range(0, 3):
            img_curr[:,:,color] = alpha_foreground * img_ontop[:,:,color] + img_curr[:,:,color] * (1 - alpha_foreground)

        return img_curr

    @staticmethod
    def rotate_image(image, angle):
        h, w = image.shape[:2]
        c_x, c_y = w//2, h//2

        M = cv2.getRotationMatrix2D((c_x, c_y), angle, 1)
        rotated = cv2.warpAffine(image, M, (w, h))

        return rotated
        
    def set_ck3_map(self):
        
        river_map = cv2.imread("images/ck3map/rivers.png").astype("uint8")
        water_map = cv2.imread("images/nasa/imgimg.png").astype("uint8")
        self.map_img_original = water_map
        self.map_img = self.map_img_original
        return None
        #return water_map
        height_map = cv2.imread("images/ck3map/heightmap.png").astype("uint8")
        provinces_map = cv2.imread("images/ck3map/provinces.png").astype("uint8")

        map = np.zeros(river_map.shape).astype("uint8")


        beach_02_mask = cv2.imread("images/ck3map/terrain/beach_02_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, beach_02_mask, (205, 235, 255))

        desert_02_mask = cv2.imread("images/ck3map/terrain/desert_02_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        desert_rocky_mask = cv2.imread("images/ck3map/terrain/desert_rocky_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        desert_wavy_01_mask = cv2.imread("images/ck3map/terrain/desert_wavy_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, desert_02_mask, (99, 173, 206))
        map = Map._overlay_rgb_mask(map, desert_wavy_01_mask, (107, 181, 222))
        map = Map._overlay_rgb_mask(map, desert_rocky_mask, (41, 90, 115))

        drylands_01_grassy_mask = cv2.imread("images/ck3map/terrain/drylands_01_grassy_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, drylands_01_grassy_mask, (49, 132, 132))
        drylands_01_mask = cv2.imread("images/ck3map/terrain/drylands_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, drylands_01_mask, (115, 189, 214))

        forest_pine_01_mask = cv2.imread("images/ck3map/terrain/forest_pine_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, forest_pine_01_mask, (49, 66, 24))
        forestfloor_mask = cv2.imread("images/ck3map/terrain/forestfloor_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, forestfloor_mask, (82, 90, 74))

        hills_01_mask = cv2.imread("images/ck3map/terrain/hills_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, hills_01_mask, (82, 99, 82))
        hills_01_rocks_mask = cv2.imread("images/ck3map/terrain/hills_01_rocks_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, hills_01_rocks_mask, (33, 107, 74))
        hills_01_rocks_medi_mask = cv2.imread("images/ck3map/terrain/hills_01_rocks_medi_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, hills_01_rocks_medi_mask, (49, 99, 115))
        hills_01_rocks_small_mask = cv2.imread("images/ck3map/terrain/hills_01_rocks_small_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, hills_01_rocks_small_mask, (41, 115, 123))

        plains_01_dry_mask = cv2.imread("images/ck3map/terrain/plains_01_dry_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, plains_01_dry_mask, (74, 132, 82))
        plains_01_dry_mud_mask = cv2.imread("images/ck3map/terrain/plains_01_dry_mud_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, plains_01_dry_mud_mask, (74, 132, 99))
        plains_01_mask = cv2.imread("images/ck3map/terrain/plains_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, plains_01_mask, (74, 165, 123))
        plains_01_noisy_mask = cv2.imread("images/ck3map/terrain/plains_01_noisy_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, plains_01_noisy_mask, (24, 123, 107))
        plains_01_rough_mask = cv2.imread("images/ck3map/terrain/plains_01_rough_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, plains_01_rough_mask, (16, 132, 90))

        steppe_01_mask = cv2.imread("images/ck3map/terrain/steppe_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._overlay_rgb_mask(map, steppe_01_mask, (99, 156, 148))

        #map, map_mask = Map._overlay_rgb_mask(map, map_mask, desert_02_colored, desert_02_mask)
        #map, map_mask = Map._overlay_rgb_mask(map, map_mask, desert_rocky_colored, desert_rocky_mask)

        #map = desert_wavy_01_colored/255 * desert_wavy_01_mask/255 + map/255
        #map_mask += desert_wavy_01_mask

        #map = desert_rocky_colored/255 * desert_rocky_mask/255 + map/255 * (1 - map_mask/255)
        #map_mask += desert_rocky_mask

        #return np.where(water_map == 255, np.ones(river_map.shape) * (255, 0, 0), map)
        return map

    def get_map_img(self, frame: int):
        return self.map_img

        # https://youtu.be/qq76LCiP2Ds



    def add_object(self, map_object: "MapObject", is_static: bool) -> None:
        if (is_static):
            self.map_img = map_object.draw(self.map_img)
            self.static_objects.append(map_object)
        else:
            self.dynamic_objects.append(map_object)

class MapObject:
    def __init__(self, x: int, y: int, img: np.array) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.angle = random.randint(0, 360)

class City(MapObject):
    def __init__(self, x: int, y: int, name: str, img_file_path="images/assets/castle1_low.png"):
        city_img = cv2.imread(img_file_path, cv2.IMREAD_UNCHANGED)
        super().__init__(x, y, city_img)

        self.name = name

    def draw(self, map_img: np.array):
        x1 = self.x - self.img.shape[1] // 2
        y1 = self.y - self.img.shape[0] // 2
        x2 = x1 + self.img.shape[1]
        y2 = y1 + self.img.shape[0]

        img_rotated = Map.rotate_image(self.img, self.angle)
        map_img[y1:y2, x1:x2] = Map._add_foreground_image(map_img[y1:y2, x1:x2], img_rotated)
        
        font = ImageFont.truetype("fonts/IMFeGPrm29P.ttf", 24)

        img_pil = Image.fromarray(map_img)
        draw = ImageDraw.Draw(img_pil)
        draw.text((self.x - self.img.shape[1], self.y + 30), self.name.upper(), font=font, fill=(0, 0, 0, 255), align="center")
        map_img = np.array(img_pil)

        return map_img


if __name__ == "__main__":
    img = Map.get_ck3_map()
    cv2.imshow('image', cv2.resize(img, (1600, 800), interpolation=cv2.INTER_LANCZOS4))
    cv2.waitKey(0)
    cv2.destroyAllWindows()