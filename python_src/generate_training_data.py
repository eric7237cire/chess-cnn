import functools
import json
import shutil
from pathlib import Path
from time import sleep
from typing import Tuple
from scipy.misc import imresize
import imageio as imageio
from skimage import color
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image, ImageOps, ImageDraw

class Config(object):

    PROJECT_DIR = Path(__file__).parent.parent
    DATA_DIR = PROJECT_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw_data"

    TRAINING_DATA_DIR = DATA_DIR / "training_data"

    PIECE_LOCATIONS_PATH = RAW_DATA_DIR / "piece_locations.json"

    PIECE_IMAGE_SHAPE = (64, 64)

def retry(retry_count=5, delay=5, allowed_exceptions=()):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for _ in range(retry_count):
                # everything in here would be the same
                try:
                    result = f(*args, **kwargs)
                    if result:
                        return result
                    else:
                        return None
                except allowed_exceptions as e:
                    pass

                print(f"waiting for {delay} seconds before retyring again")
                sleep(delay)


        return wrapper
    return decorator

def enum_fen(fen: str) -> Tuple[chr, int, int]:

    split_fen = fen.split(' ')

    fen_piece_locations = split_fen[0]

    is_board_reversed = split_fen[1] == 'b'

    for row, fen_row_pieces in enumerate(fen_piece_locations.split('/')):

        # print(row)

        col = 0
        for fen_char in fen_row_pieces:
            if str.isdigit(fen_char):
                col += int(fen_char)
            else:

                if is_board_reversed:
                    adj_row = 7 - row
                    adj_col = 7 - col
                else:
                    adj_col = col
                    adj_row = row

                print(f"Row: {adj_row} Col: {adj_col} {fen_char}")

                yield (fen_char, adj_row, adj_col)

                col += 1


@retry(allowed_exceptions=PermissionError, delay=0.25)
def recreate_dir(dir: Path):

    if not str(dir).startswith(r"E:\git\chess-cnn\data"):
        raise Exception("Shouldn't delete just anything: "  + str(dir))

    if dir.exists():
        shutil.rmtree(dir)

    dir.mkdir(exist_ok=False)



if __name__ == "__main__":

    recreate_dir(Config.TRAINING_DATA_DIR)

    with open(Config.PIECE_LOCATIONS_PATH) as json_data:
        d = json.load(json_data)

        for file_index, raw_data_fn in enumerate(d):

            print(raw_data_fn)

            board_array: np.array = imageio.imread(Config.RAW_DATA_DIR / raw_data_fn,
                                         format = "png",
                                         pilmode = "I",)
            #as_gray = True)

            board_array = board_array.astype(np.uint8)

            print(board_array.dtype)

            # We don't need the alpha channel
            #board_array = board_array[:, :, 0:3]

            print(board_array.shape)

            # And we don't need colors
            #board_array = color.rgb2gray(board_array)

            square_width = board_array.shape[1] / 8
            square_height = board_array.shape[0] / 8

            if False:
                plt.imshow(board_array)
                plt.title(raw_data_fn)
                plt.show()

            fen = d[raw_data_fn]

            for fen_char, row, col in enum_fen(fen):

                print(f"Row: {row} Col: {col} {fen_char}")

                piece_image = board_array[int(round(row * square_height)):int(round(row * square_height + square_height)),
                              int(round(col * square_width)): int(round((col + 1) * square_width))]

                if False:
                    plt.imshow(piece_image)
                    plt.title(fen_char)
                    plt.show()

                # https://pillow.readthedocs.io/en/latest/handbook/concepts.html#modes
                image_resized = imresize(piece_image, Config.PIECE_IMAGE_SHAPE, 'bilinear', 'I')

                image_resized = image_resized.astype(np.uint8)

                image_variations = [
                    image_resized,
                ]

                for idx, img in enumerate(image_variations):
                    file_name =  f"{fen_char}_{Path(raw_data_fn).stem}_{row}_{col}_{idx}.png"
                    file_path = Config.TRAINING_DATA_DIR / file_name

                    imageio.imwrite(file_path, img, "png")

