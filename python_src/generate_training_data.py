import json
from pathlib import Path

import imageio as imageio
import matplotlib.pyplot as plt

class Config(object):

    PROJECT_DIR = Path(__file__).parent.parent
    DATA_DIR = PROJECT_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw_data"

    PIECE_LOCATIONS_PATH = RAW_DATA_DIR / "piece_locations.json"


if __name__ == "__main__":

    with open(Config.PIECE_LOCATIONS_PATH) as json_data:
        d = json.load(json_data)

        for file_index, raw_data_fn in enumerate(d):

            if file_index < 3:
                continue

            print(raw_data_fn)

            board_array = imageio.imread(Config.RAW_DATA_DIR / raw_data_fn)

            print(board_array.shape)

            square_width = board_array.shape[1] / 8
            square_height = board_array.shape[0] / 8

            if False:
                plt.imshow(board_array)
                plt.title(raw_data_fn)
                plt.show()

            fen = d[raw_data_fn]

            split_fen = fen.split(' ')

            fen_piece_locations = split_fen[0]

            is_board_reversed = split_fen[1] == 'b'

            for row, fen_row_pieces in enumerate(fen_piece_locations.split('/')):

                #print(row)

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

                        piece_image = board_array[int(round(adj_row * square_height)):int(round(adj_row * square_height + square_height)),
                                      int(round(adj_col * square_width)): int(round((adj_col + 1) * square_width))]

                        plt.imshow(piece_image)
                        plt.title(fen_char)
                        plt.show()

                        col += 1