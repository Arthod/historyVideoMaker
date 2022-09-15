# Combine images to form a map (3d map?)

import os
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
    def _overlay_rgb_mask(img_curr, img_path, color_rgb):
        mask_new = cv2.imread(img_path, flags=cv2.IMREAD_GRAYSCALE)
        #mask_new = np.minimum(mask_new.astype("uint32") * 2, 255).astype("uint8")
        return np.minimum(np.stack((
            mask_new/255 * color_rgb[2] + img_curr[:,:, 0],
            mask_new/255 * color_rgb[1] + img_curr[:,:, 1],
            mask_new/255 * color_rgb[0] + img_curr[:,:, 2]
        ), axis=2), 255).astype("uint8")

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

    def generate_terrain_map(self):
        terrain_map = np.zeros(cv2.imread("images/ck3map/terrain.png").astype("uint8").shape)

        # Beach
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/beach_02_mask.png", (255, 235, 205))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/beach_02_mediterranean_mask.png", (255, 235, 205))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/beach_02_pebbles_mask.png", (255, 235, 205))

        # Coastline
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/coastline_cliff_brown_mask.png", (87, 89, 39))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/coastline_cliff_desert_mask.png", (207, 171, 119))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/coastline_cliff_grey_mask.png", (169, 161, 78))

        # Desert
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/desert_01_mask.png", (219, 192, 113))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/desert_02_mask.png", (219, 201, 119))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/desert_cracked_mask.png", (223, 190, 113))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/desert_flat_01_mask.png", (231, 198, 117))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/desert_rocky_mask.png", (143, 118, 54))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/desert_wavy_01_larger_mask.png", (218, 191, 112))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/desert_wavy_01_mask.png", (227, 197, 124))

        # Drylands
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/drylands_01_cracked_mask.png", (145, 123, 94))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/drylands_01_grassy_mask.png", (154, 136, 102))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/drylands_01_mask.png", (190, 175, 92))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/drylands_grass_clean_mask.png", (190, 175, 92)) # Unfinished

        # Farmland, Floodplains & Forest
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/farmland_01_mask.png", (115, 150, 68))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/floodplains_01_mask.png", (43, 68, 21)) # Unfinished?
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/forest_jungle_01_mask.png", (114, 119, 25))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/forest_leaf_01_mask.png", (117, 149, 66))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/forest_pine_01_mask.png", (53, 104, 61))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/forestfloor_02_mask.png", (82, 90, 74)) # Unfinished
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/forestfloor_mask.png", (82, 90, 74)) # Unfinished

        # Hills
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/hills_01_mask.png", (30, 37, 13))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/hills_01_rocks_mask.png", (82, 82, 43))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/hills_01_rocks_medi_mask.png", (91, 74, 115))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/hills_01_rocks_small_mask.png", (95, 89, 56))

        # India and Medi
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/india_farmlands_mask.png", (87, 96, 60))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/medi_dry_mud_mask.png", (93, 89, 50))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/medi_farmlands_mask.png", (98, 110, 65))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/medi_grass_01_mask.png", (88, 92, 55))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/medi_grass_02_mask.png", (41, 115, 123)) # Unfinished
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/medi_hills_01_mask.png", (41, 115, 123)) # Unfinished
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/medi_lumpy_grass_mask.png", (41, 115, 123)) # Unfinished
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/medi_noisy_grass_mask.png", (79, 75, 44))

        # Mountain
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mountain_02_b_mask.png", (74, 70, 42))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mountain_02_c_mask.png", (30, 29, 15))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mountain_02_c_snow_mask.png", (255, 255, 255))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mountain_02_d_desert_mask.png", (99, 83, 53))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mountain_02_d_mask.png", (37, 41, 19))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mountain_02_d_snow_mask.png", (226, 225, 219))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mountain_02_d_valleys_mask.png", (50, 60, 24))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mountain_02_desert_c_mask.png", (120, 104, 68))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mountain_02_desert_mask.png", (35, 28, 17))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mountain_02_mask.png", (39, 35, 20))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mountain_02_snow_mask.png", (179, 177, 166))

        # Misc
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/mud_wet_01_mask.png", (42, 50, 17))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/northern_hills_01_mask.png", (30, 37, 13)) # Unfinished
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/northern_plains_01_mask.png", (98, 100, 64))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/oasis_mask.png", (82, 99, 85)) # Unfinished?
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/snow_mask.png", (231, 236, 233))

        # Plains
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/plains_01_dry_mask.png", (34, 39, 16))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/plains_01_dry_mud_mask.png", (32, 41, 15))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/plains_01_mask.png", (52, 71, 31))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/plains_01_noisy_mask.png", (84, 99, 18))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/plains_01_rough_mask.png", (61, 73, 35))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/plains_01_desat_mask.png", (34, 39, 16)) # Unfinished

        # Steppe
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/steppe_01_mask.png", (76, 73, 41))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/steppe_bushes_mask.png", (21, 46, 6))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/steppe_rocks_mask.png", (78, 70, 43))

        # Wetlands
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/wetlands_02_mask.png", (64, 76, 26))
        terrain_map = Map._overlay_rgb_mask(terrain_map, "images/ck3map/terrain/wetlands_02_mud_mask.png", (34, 41, 14))
            
        return terrain_map
        
    def set_ck3_map(self):
        
        # Terrain map
        if (os.path.exists("metadata/terrain_map.png")):
            terrain_map = cv2.imread("metadata/terrain_map.png").astype("uint8")
        else:
            terrain_map = self.generate_terrain_map()
            cv2.imwrite("metadata/terrain_map.png", terrain_map)
            print("Generating metadata - terrain map")

        map = terrain_map

        river_map = cv2.imread("images/ck3map/rivers.png").astype("uint8")
        water_map = cv2.imread("images/ck3map/water.png").astype("uint8")
        height_map = cv2.imread("images/ck3map/heightmap.png").astype("uint8")
        provinces_map = cv2.imread("images/ck3map/provinces.png").astype("uint8")

            
        self.map_img_original = map
        self.map_img = self.map_img_original
        return self.map_img_original

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


        x = self.x - self.img.shape[1]
        y = self.y + 30
        # Thin border
        draw.text((x - 1, y), self.name.upper(), font=font, fill=(0, 0, 0, 255), align="center")
        draw.text((x + 1, y), self.name.upper(), font=font, fill=(0, 0, 0, 255), align="center")
        draw.text((x, y - 1), self.name.upper(), font=font, fill=(0, 0, 0, 255), align="center")
        draw.text((x, y + 1), self.name.upper(), font=font, fill=(0, 0, 0, 255), align="center")

        # Thick border
        draw.text((x - 1, y - 1), self.name.upper(), font=font, fill=(0, 0, 0, 255), align="center")
        draw.text((x + 1, y - 1), self.name.upper(), font=font, fill=(0, 0, 0, 255), align="center")
        draw.text((x - 1, y + 1), self.name.upper(), font=font, fill=(0, 0, 0, 255), align="center")
        draw.text((x + 1, y + 1), self.name.upper(), font=font, fill=(0, 0, 0, 255), align="center")

        draw.text((x, y), self.name.upper(), font=font, fill=(255, 255, 255, 255), align="center")
        map_img = np.array(img_pil)

        return map_img


if __name__ == "__main__":
    img = Map.get_ck3_map()
    cv2.imshow('image', cv2.resize(img, (1600, 800), interpolation=cv2.INTER_LANCZOS4))
    cv2.waitKey(0)
    cv2.destroyAllWindows()