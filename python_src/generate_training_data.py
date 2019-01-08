import json
from pathlib import Path

import imageio as imageio
import joblib
import numpy as np
from config import Config
from util.dto import ChessBoard
from util.file import recreate_dir
from util.chess import enum_fen

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

            board = ChessBoard(image_array=board_array)

            # We don't need the alpha channel
            # board_array = board_array[:, :, 0:3]

            print(board_array.shape)

            if False:
                plt.imshow(board_array)
                plt.title(raw_data_fn)
                plt.show()

            fen = d[raw_data_fn]

            include_spaces = file_index == 4

            for fen_char, row, col in enum_fen(fen, include_empty_spaces=include_spaces):

                # print(f"Row: {row} Col: {col} {fen_char}")

                for row_offset in range(-Config.IMAGE_VARIATION_MAX_OFFSET, Config.IMAGE_VARIATION_MAX_OFFSET + 1, 1):
                    for col_offset in range(-Config.IMAGE_VARIATION_MAX_OFFSET, Config.IMAGE_VARIATION_MAX_OFFSET + 1,
                                            1):

                        piece_image = board.get_piece_array(row=row, col=col,
                                                            row_offset=row_offset,
                                                            col_offset=col_offset)

                        if piece_image is None:
                            continue

                        if False:
                            plt.imshow(piece_image)
                            plt.title(fen_char)
                            plt.show()

                        file_name = f"{Path(raw_data_fn).stem}_{row}_{col}_{fen_char}_{row_offset}_{col_offset}.png"
                        file_path = Config.TRAINING_DATA_DIR / file_name

                        imageio.imwrite(file_path, piece_image, "png")

                        X.append(piece_image)

                        Y.append(Config.CLASS_TO_PIECE.index(fen_char))

                        if len(X) % 500 == 0:
                            print(f"X is now {len(X)}")

    X = np.stack(X, axis=0)
    Y = np.stack(Y, axis=0)

    joblib.dump(X, Config.TRAINING_DATA_DIR / "X.dat")
    joblib.dump(Y, Config.TRAINING_DATA_DIR / "Y.dat")
