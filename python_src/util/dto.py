from typing import Dict, Tuple, Union

from scipy.misc import imresize
from shapely.geometry import Polygon
import attr
import numpy as np

from config import Config


@attr.s(repr=False)
class BoundingBox(object):
    min_x: float = attr.ib(default=None)
    min_y: float = attr.ib(default=None)
    max_x: float = attr.ib(default=None)
    max_y: float = attr.ib(default=None)

    def clip_2d_array(self, image_yx_array):
        return image_yx_array[
               int(self.min_y):int(self.max_y) + 1,
               int(self.min_x):int(self.max_x) + 1]

    def center_yx(self):
        return self.min_y + (self.max_y - self.min_y) / 2, self.min_x + (self.max_x - self.min_x) / 2

    def __repr__(self):
        return "Bounding box.  Y {} to {}.  X {} to {}".format(self.min_y, self.max_y, self.min_x, self.max_x)


@attr.s
class Contour(object):
    bounding_box: BoundingBox = attr.ib(default=None)

    # 2d array in y/x order
    points_array: Dict[Tuple[int, int], float] = attr.ib(default=None)

    polygon: Polygon = attr.ib(default=None)

    def set_points_array(self, points_array):
        self.points_array = points_array

        if len(self.points_array) >= 4:
            self.polygon = Polygon(self.get_contour_xy())
            # self.polygon = self.polygon.simplify(tolerance=0.2, preserve_topology=False)
        else:
            self.polygon = None

    def get_contour_xy(self):
        """
        Contours are in y,x

        :return: same points x,y
        """
        # https://stackoverflow.com/questions/4857927/swapping-columns-in-a-numpy-array
        return self.points_array[:, [1, 0]]


@attr.s
class ChessBoard(object):
    image_array: np.ndarray = attr.ib(default=None)

    square_width: int = attr.ib(default=None)
    square_height: int = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.square_width = self.image_array.shape[1] / 8
        self.square_height = self.image_array.shape[0] / 8

    def get_piece_array(self, row: int, col: int, row_offset: int = 0, col_offset: int = 0) -> Union[np.ndarray, None]:
        piece_bounds_tuple = (row * self.square_height + row_offset,
                              row * self.square_height + self.square_height + row_offset,
                              col * self.square_width + col_offset,
                              (col + 1) * self.square_width + col_offset
                              )
        piece_img_bounds = np.asarray(piece_bounds_tuple)
        piece_img_bounds = np.rint(piece_img_bounds)
        piece_img_bounds = piece_img_bounds.astype(np.int32)

        if np.min(piece_img_bounds) < 0:
            return None

        piece_image = self.image_array[
                      piece_img_bounds[0]:piece_img_bounds[1],
                      piece_img_bounds[2]:piece_img_bounds[3]]

        # https://pillow.readthedocs.io/en/latest/handbook/concepts.html#modes
        image_resized = imresize(piece_image, Config.PIECE_IMAGE_SHAPE, 'bilinear', 'I')

        image_resized = image_resized.astype(np.uint8)

        return image_resized
