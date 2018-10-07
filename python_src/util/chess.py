from typing import Tuple


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
