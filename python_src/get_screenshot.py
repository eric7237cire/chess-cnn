import logging
from pathlib import Path
from typing import List

import imageio
import joblib
from PIL import ImageOps
from keras.engine.saving import model_from_json

from config import Config
from util.dto import Contour, ChessBoard
from util.image import find_contours, display_image_with_contours
from util.python import init_logger
from util.windows import capture_screenshot
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

init_logger()

logger.info("hello")

Config.SCREENSHOT_DIR.mkdir(exist_ok=True)

screenshot_path: Path = Config.SCREENSHOT_DIR / 'ss.png'

if not screenshot_path.exists():
    capture_screenshot(windows_title="Chess Tactics",
                       output_file_path=str(screenshot_path))

ss_array: np.array = imageio.imread(screenshot_path, format="png", pilmode="I")

contours:List[Contour] = list(find_contours(grey_array=ss_array,
                              value_threshold=60,
                              min_width=300,
                              min_height=300,
                              max_width=1000, max_height=1000, display=False))

logger.debug(f"Contours found {len(contours)}")


chessboard_img = contours[0].bounding_box.clip_2d_array(image_yx_array=ss_array)

border_width = 16
chessboard_img = chessboard_img[ border_width: -border_width, border_width: -border_width]

display_image_with_contours(grey_array=chessboard_img, contours=[])
#display_image_with_contours(ss_array, [c.points_array for c in contours])



# plt.imshow(ss_array)
# fig, ax = plt.subplots()

# ax.imshow(ss_array, interpolation='nearest', cmap=plt.cm.gray)

# plt.title("SS")
# plt.show()

model_structure = Config.CHESS_PIECE_MODEL_STRUCTURE_PATH.read_text()
model = model_from_json(model_structure)

board = ChessBoard(chessboard_img)

X = []

for row in range(0, 8):
    for col in range(0, 8):
        X.append(board.get_piece_array(row,col))

X = np.stack(X, axis=0)
X = X.reshape(list(X.shape) + [1])

Y = model.predict(X)

print(Y)