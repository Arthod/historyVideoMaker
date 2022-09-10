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
        
    def get_ck3_map():

        river_map = cv2.imread("images/ck3map/rivers.png").astype("uint8")
        water_map = cv2.imread("images/ck3map/water.png").astype("uint8")
        height_map = cv2.imread("images/ck3map/heightmap.png").astype("uint8")
        provinces_map = cv2.imread("images/ck3map/provinces.png").astype("uint8")

        texture_map = np.zeros(river_map.shape)
        desert_02_mask = cv2.imread("images/ck3map/terrain/desert_02_mask.png")
        desert_02_colored = np.stack((
            np.round(desert_02_mask[..., 0]/255 * 99),
            np.round(desert_02_mask[..., 1]/255 * 173),
            np.round(desert_02_mask[..., 2]/255 * 206)
            ), axis=2).astype("uint8")

        desert_rocky_mask = cv2.imread("images/ck3map/terrain/desert_rocky_mask.png")
        desert_rocky_colored = np.stack((
            np.round(desert_rocky_mask[..., 0]/255 * 41),
            np.round(desert_rocky_mask[..., 1]/255 * 90),
            np.round(desert_rocky_mask[..., 2]/255 * 115)
            ), axis=2).astype("uint8")

        desert_wavy_01_mask = cv2.imread("images/ck3map/terrain/desert_wavy_01_mask.png")
        desert_wavy_01_colored = np.stack((
            np.round(desert_wavy_01_mask[..., 0]/255 * 107),
            np.round(desert_wavy_01_mask[..., 1]/255 * 181),
            np.round(desert_wavy_01_mask[..., 2]/255 * 222)
            ), axis=2).astype("uint8")

        map = np.zeros(river_map.shape)
        map_mask = np.zeros(river_map.shape)

        map = desert_wavy_01_colored/255 * desert_wavy_01_mask/255 + map/255
        map_mask += desert_wavy_01_mask

        map = desert_rocky_colored/255 * desert_rocky_mask/255 + map/255 * (1 - map_mask/255)
        map_mask += desert_rocky_mask

        #return np.where(water_map == 255, np.ones(river_map.shape) * (255, 0, 0), map)
        return map


if __name__ == "__main__":
    img = Map.get_ck3_map()
    cv2.imshow('image', cv2.resize(img, (1600, 800), interpolation=cv2.INTER_CUBIC))
    cv2.waitKey(0)
    cv2.destroyAllWindows()