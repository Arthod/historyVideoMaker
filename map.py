# Combine images to form a map (3d map?)

import cv2
import numpy as np

class Map:
    def get_ck2_map():

        colormap = cv2.imread("images/ck2map/colormap.png").astype("uint8")
        colormap_water = cv2.imread("images/ck2map/colormap_water.png").astype("uint8")
        rivers = cv2.imread("images/ck2map/rivers.png").astype("uint8")
        terrain = cv2.imread("images/ck2map/terrain.png").astype("uint8")
        topology = cv2.imread("images/ck2map/topology.png").astype("uint8")

        return colormap

    def get_nasa_map():
        b1 = cv2.imread("images/nasaTest/b1.png")
        c1 = cv2.imread("images/nasaTest/c1.png")
        b1_top = cv2.imread("images/nasaTest/b1_top.png")
        c1_top = cv2.imread("images/nasaTest/c1_top.png")

        terrain_map = np.hstack((b1, c1))
        topology_map = np.hstack((b1_top, c1_top))


        
        return terrain_map


    def _add_mask_ontop(img_curr, mask_new, color_bgr):
        img_new = np.stack((
            np.round(mask_new/255 * color_bgr[0]),# + (1 - mask_curr/255) * img_curr[...,0]/255),
            np.round(mask_new/255 * color_bgr[1]),# + (1 - mask_curr/255) * img_curr[...,1]/255),
            np.round(mask_new/255 * color_bgr[2])# + (1 - mask_curr/255) * img_curr[...,2]/255)
            ), axis=2).astype("uint8")
        #img_curr = np.multiply(img/255, mask_new/255) + np.multiply(img_curr, (1 - mask_curr/255))
        img_curr = cv2.addWeighted(img_curr, 1, img_new, 1, 0)# = mask_curr + mask_new#np.minimum(mask_curr + mask_new, 255)

        return img_curr
        
    def get_ck3_map():
        
        river_map = cv2.imread("images/ck3map/rivers.png").astype("uint8")
        water_map = cv2.imread("images/ck3map/water.png").astype("uint8")
        return water_map
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


if __name__ == "__main__":
    img = Map.get_ck3_map()
    cv2.imshow('image', cv2.resize(img, (1600, 800), interpolation=cv2.INTER_CUBIC))
    cv2.waitKey(0)
    cv2.destroyAllWindows()