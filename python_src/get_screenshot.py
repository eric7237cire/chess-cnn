from pathlib import Path

import imageio

from config import Config
from util.windows import capture_screenshot
import numpy as np
import matplotlib.pyplot as plt

Config.SCREENSHOT_DIR.mkdir(exist_ok=True)

screenshot_path : Path=Config.SCREENSHOT_DIR / 'ss.png'

if not screenshot_path.exists():

    capture_screenshot(windows_title="Chess Tactics",
                   output_file_path=str(screenshot_path))



ss_array: np.array = imageio.imread(screenshot_path, format="png",pilmode="I")

plt.imshow(ss_array)
fig, ax = plt.subplots()

ax.imshow(ss_array, interpolation='nearest', cmap=plt.cm.gray)

plt.title("SS")
plt.show()
