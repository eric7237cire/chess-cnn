import json
from pathlib import Path

import imageio as imageio
import joblib
import numpy as np
from scipy.misc import imresize

from config import Config
from util.file import recreate_dir


if __name__ == "__main__":

    recreate_dir(Config.TRAINING_DATA_DIR)

    X = []
    Y = []

    with open(Config.PIECE_LOCATIONS_PATH) as json_data:
        d = json.load(json_data)

        for file_index, raw_data_fn in enumerate(d):

            print(raw_data_fn)

            board_array: np.array = imageio.imread(Config.RAW_DATA_DIR / raw_data_fn,
                                                   format="png",
                                                   pilmode="I", )
            # as_gray = True)

            board_array = board_array.astype(np.uint8)

            print(board_array.dtype)

            # We don't need the alpha channel
            # board_array = board_array[:, :, 0:3]

            print(board_array.shape)

            #board_array = ImageOps.expand(image=board_array, border=Config.IMAGE_VARIATION_MAX_OFFSET, fill=0)

            # And we don't need colors
            # board_array = color.rgb2gray(board_array)

            square_width = board_array.shape[1] / 8
            square_height = board_array.shape[0] / 8

            if False:
                plt.imshow(board_array)
                plt.title(raw_data_fn)
                plt.show()

            fen = d[raw_data_fn]

            for fen_char, row, col in enum_fen(fen):

                #print(f"Row: {row} Col: {col} {fen_char}")

                for row_offset in range(-Config.IMAGE_VARIATION_MAX_OFFSET, Config.IMAGE_VARIATION_MAX_OFFSET + 1, 1):
                    for col_offset in range(-Config.IMAGE_VARIATION_MAX_OFFSET, Config.IMAGE_VARIATION_MAX_OFFSET + 1,
                                            1):

                        piece_bounds_tuple = (row * square_height + row_offset,
                             row * square_height + square_height + row_offset,
                             col * square_width + col_offset,
                             (col + 1) * square_width + col_offset
                             )
                        piece_img_bounds = np.asarray(piece_bounds_tuple)
                        piece_img_bounds = np.rint(piece_img_bounds)
                        piece_img_bounds = piece_img_bounds.astype(np.int32)

                        if np.min( piece_img_bounds ) < 0:
                            continue

                        piece_image = board_array[piece_img_bounds[0]:piece_img_bounds[1],
                                      piece_img_bounds[2]:piece_img_bounds[3]]

                        if False:
                            plt.imshow(piece_image)
                            plt.title(fen_char)
                            plt.show()

                        #print(piece_image.shape)

                        # https://pillow.readthedocs.io/en/latest/handbook/concepts.html#modes
                        image_resized = imresize(piece_image, Config.PIECE_IMAGE_SHAPE, 'bilinear', 'I')

                        image_resized = image_resized.astype(np.uint8)

                        file_name = f"{fen_char}_{Path(raw_data_fn).stem}_{row}_{col}_{row_offset}_{col_offset}.png"
                        file_path = Config.TRAINING_DATA_DIR / file_name

                        imageio.imwrite(file_path, image_resized, "png")

                        X.append(image_resized)

                        Y.append( Config.PIECE_TO_CLASS[fen_char] )

                        if len(X) % 500 == 0:
                            print(f"X is now {len(X)}")

    X = np.stack(X, axis=0)
    Y = np.stack(Y, axis=0)

    joblib.dump(X, Config.TRAINING_DATA_DIR / "X.dat")
    joblib.dump(Y, Config.TRAINING_DATA_DIR / "Y.dat")


