import json
from pathlib import Path


class Config(object):

    PROJECT_DIR = Path(__file__).parent.parent
    DATA_DIR = PROJECT_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw_data"

    PIECE_LOCATIONS_PATH = RAW_DATA_DIR / "piece_locations.json"


if __name__ == "__main__":

    with open(Config.PIECE_LOCATIONS_PATH) as json_data:
        d = json.load(json_data)

        for raw_data_fn in d:
            print(raw_data_fn)

            fen = d[raw_data_fn]

            fen_piece_locations = fen.split(' ')[0]

            for row, fen_row_pieces in enumerate(fen_piece_locations.split('/')):

                print(row)

                col = 0
                for fen_char in fen_row_pieces:
                    if str.isdigit(fen_char):
                        col += int(fen_char)
                    else:
                        print(fen_char)
                        col += 1