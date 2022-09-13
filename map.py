# Combine images to form a map (3d map?)

import cv2
import numpy as np

class Map:
    def __init__(self):
        self.map_img = None
        self.static_objects: list[MapObject] = []
        self.dynamic_objects: list[MapObject] = []

    @staticmethod
    def _add_mask_ontop(img_curr, mask_new, color_bgr):
        img_new = np.stack((
            np.round(mask_new/255 * color_bgr[0]),# + (1 - mask_curr/255) * img_curr[...,0]/255),
            np.round(mask_new/255 * color_bgr[1]),# + (1 - mask_curr/255) * img_curr[...,1]/255),
            np.round(mask_new/255 * color_bgr[2])# + (1 - mask_curr/255) * img_curr[...,2]/255)
            ), axis=2).astype("uint8")
        #img_curr = np.multiply(img/255, mask_new/255) + np.multiply(img_curr, (1 - mask_curr/255))
        img_curr = cv2.addWeighted(img_curr, 1, img_new, 1, 0)# = mask_curr + mask_new#np.minimum(mask_curr + mask_new, 255)

        return img_curr

    @staticmethod
    def _add_mask_ontop2(img_curr, img_new, mask_new):
        img_new = np.stack((
            np.round(mask_new/255 * color_bgr[0]),# + (1 - mask_curr/255) * img_curr[...,0]/255),
            np.round(mask_new/255 * color_bgr[1]),# + (1 - mask_curr/255) * img_curr[...,1]/255),
            np.round(mask_new/255 * color_bgr[2])# + (1 - mask_curr/255) * img_curr[...,2]/255)
            ), axis=2).astype("uint8")
        #img_curr = np.multiply(img/255, mask_new/255) + np.multiply(img_curr, (1 - mask_curr/255))
        img_curr = cv2.addWeighted(img_curr, 1, img_new, 1, 0)# = mask_curr + mask_new#np.minimum(mask_curr + mask_new, 255)

        return img_curr
        
    def set_ck3_map(self):
        
        river_map = cv2.imread("images/ck3map/rivers.png").astype("uint8")
        water_map = cv2.imread("images/ck3map/water.png").astype("uint8")
        self.map_img_original = water_map
        self.map_img = self.map_img_original
        return None
        #return water_map
        height_map = cv2.imread("images/ck3map/heightmap.png").astype("uint8")
        provinces_map = cv2.imread("images/ck3map/provinces.png").astype("uint8")

        map = np.zeros(river_map.shape).astype("uint8")


        beach_02_mask = cv2.imread("images/ck3map/terrain/beach_02_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, beach_02_mask, (205, 235, 255))

        desert_02_mask = cv2.imread("images/ck3map/terrain/desert_02_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        desert_rocky_mask = cv2.imread("images/ck3map/terrain/desert_rocky_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        desert_wavy_01_mask = cv2.imread("images/ck3map/terrain/desert_wavy_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, desert_02_mask, (99, 173, 206))
        map = Map._add_mask_ontop(map, desert_wavy_01_mask, (107, 181, 222))
        map = Map._add_mask_ontop(map, desert_rocky_mask, (41, 90, 115))

        drylands_01_grassy_mask = cv2.imread("images/ck3map/terrain/drylands_01_grassy_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, drylands_01_grassy_mask, (49, 132, 132))
        drylands_01_mask = cv2.imread("images/ck3map/terrain/drylands_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, drylands_01_mask, (115, 189, 214))

        forest_pine_01_mask = cv2.imread("images/ck3map/terrain/forest_pine_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, forest_pine_01_mask, (49, 66, 24))
        forestfloor_mask = cv2.imread("images/ck3map/terrain/forestfloor_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, forestfloor_mask, (82, 90, 74))

        hills_01_mask = cv2.imread("images/ck3map/terrain/hills_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, hills_01_mask, (82, 99, 82))
        hills_01_rocks_mask = cv2.imread("images/ck3map/terrain/hills_01_rocks_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, hills_01_rocks_mask, (33, 107, 74))
        hills_01_rocks_medi_mask = cv2.imread("images/ck3map/terrain/hills_01_rocks_medi_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, hills_01_rocks_medi_mask, (49, 99, 115))
        hills_01_rocks_small_mask = cv2.imread("images/ck3map/terrain/hills_01_rocks_small_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, hills_01_rocks_small_mask, (41, 115, 123))

        plains_01_dry_mask = cv2.imread("images/ck3map/terrain/plains_01_dry_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, plains_01_dry_mask, (74, 132, 82))
        plains_01_dry_mud_mask = cv2.imread("images/ck3map/terrain/plains_01_dry_mud_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, plains_01_dry_mud_mask, (74, 132, 99))
        plains_01_mask = cv2.imread("images/ck3map/terrain/plains_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, plains_01_mask, (74, 165, 123))
        plains_01_noisy_mask = cv2.imread("images/ck3map/terrain/plains_01_noisy_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, plains_01_noisy_mask, (24, 123, 107))
        plains_01_rough_mask = cv2.imread("images/ck3map/terrain/plains_01_rough_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, plains_01_rough_mask, (16, 132, 90))

        steppe_01_mask = cv2.imread("images/ck3map/terrain/steppe_01_mask.png", flags=cv2.IMREAD_GRAYSCALE)
        map = Map._add_mask_ontop(map, steppe_01_mask, (99, 156, 148))

        #map, map_mask = Map._add_mask_ontop(map, map_mask, desert_02_colored, desert_02_mask)
        #map, map_mask = Map._add_mask_ontop(map, map_mask, desert_rocky_colored, desert_rocky_mask)

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
            x1 = map_object.x - map_object.img.shape[1] // 2
            y1 = map_object.y - map_object.img.shape[0] // 2
            x2 = x1 + map_object.img.shape[1]
            y2 = y1 + map_object.img.shape[0]

            self.map_img[y1:y2, x1:x2] = self.map_img[y1:y2, x1:x2] + map_object.img * map_object.img_mask
            self.static_objects.append(map_object)
        else:
            self.dynamic_objects.append(map_object)

class MapObject:
    def __init__(self, x: int, y: int, img: np.array, img_mask: np.array) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.img_mask = img_mask

class City(MapObject):
    def __init__(self, x: int, y: int, name: str, img_file_path="images/assets/castle1_low.png"):
        city_img = cv2.imread(img_file_path)
        city_img_mask = cv2.cvtColor(city_img, cv2.COLOR_BGR2GRAY)
        super().__init__(x, y, city_img, city_img_mask)

        self.name = name


if __name__ == "__main__":
    img = Map.get_ck3_map()
    cv2.imshow('image', cv2.resize(img, (1600, 800), interpolation=cv2.INTER_CUBIC))
    cv2.waitKey(0)
    cv2.destroyAllWindows()