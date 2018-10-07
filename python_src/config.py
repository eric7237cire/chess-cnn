
class Config(object):
    PROJECT_DIR = Path(__file__).parent.parent
    DATA_DIR = PROJECT_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw_data"

    TRAINING_DATA_DIR = DATA_DIR / "training_data"

    PIECE_LOCATIONS_PATH = RAW_DATA_DIR / "piece_locations.json"

    PIECE_IMAGE_SHAPE = (64, 64)

    # Max amt of pixels to shift images during training
    IMAGE_VARIATION_MAX_OFFSET = 5

    PIECE_TO_CLASS = {
        'k': 0,
        'K': 0,
        'q': 1,
        'Q': 1,
        'b': 2,
        'B': 2,
        'n': 3,
        'N': 3,
        'r': 4,
        'R': 4,
        'p': 5,
        'P': 5,

    }