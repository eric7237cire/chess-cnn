import logging

from skimage import measure

from util.dto import BoundingBox, Contour
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)


def display_image_with_contours(grey_array, contours):
    # Display the image and plot all contours found
    fig, ax = plt.subplots()

    if grey_array is not None:
        ax.imshow(grey_array, interpolation='nearest', cmap=plt.cm.gray)

    for n, contour in enumerate(contours):
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

    ax.axis('image')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()


def find_contours(
        grey_array, min_width=5, max_width=15,
        min_height=5, max_height=100,
        value_threshold=150,
        fully_connected="low",
        display=False
):
    """
    :return:  iterable of contours in card
    """
    #logger.debug("hello")
    # grey_array[grey_array < 150] = 0
    # grey_array[grey_array >= 150] = 255

    if grey_array is None or grey_array.ndim != 2:
        logger.warning("Not a valid array passed to find_contours")
        return

    # http://scikit-image.org/docs/dev/auto_examples/edges/plot_contours.html?highlight=find_contours
    all_contours = measure.find_contours(grey_array, level=value_threshold, fully_connected=fully_connected)

    # Todo find inner shapes and subtract from polygon
    contour_list = []

    for points_array in all_contours:

        b = BoundingBox()
        b.min_y, b.min_x = np.min(points_array, axis=0)
        b.max_y, b.max_x = np.max(points_array, axis=0)

        c = Contour()
        c.bounding_box = b

        if not np.array_equal(points_array[0], points_array[-1]):
            points_array = np.append(points_array, np.expand_dims(points_array[0], axis=0), axis=0)

        c.set_points_array(points_array)

        contour_list.append(c)

    contour_list = sorted(contour_list, key=lambda x: x.bounding_box.min_x)

    if display:
        display_image_with_contours(grey_array, [c.points_array for c in contour_list])

    for idx, c in enumerate(contour_list):

        if c is None:
            continue

        width = c.bounding_box.max_x - c.bounding_box.min_x
        height = c.bounding_box.max_y - c.bounding_box.min_y

        if width < min_width or width > max_width:
            # logger.debug(f"Skipping contour #{idx}: {c} due to width")
            continue

        if height < min_height or height > max_height:
            # logger.debug(f"Skipping contour #{idx}: {c} due to height")
            continue

        # print(f"Found contour @ {min_x},{min_y} Width={width} Height={height} Numpoints={len(contour)}")

        if display:
            # display_image_with_contours(grey_array, [c.points_array ])
            pass

        if not c.polygon.is_valid:
            logger.warning("Polygon is not valid")
            continue

        # See if any additional contours fit 100% inside
        for idx2 in range(idx + 1, len(contour_list)):
            c2 = contour_list[idx2]

            if c2 is None:
                continue

            if c2.polygon is not None and c.polygon.contains(c2.polygon) and c2.polygon.is_valid:
                c.polygon = c.polygon.difference(c2.polygon)
                # don't return it in future runs
                contour_list[idx2] = None
            elif c2.bounding_box.min_x > c.bounding_box.max_x:
                break

        yield c
