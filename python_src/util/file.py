import shutil
from pathlib import Path

from .python import retry


@retry(allowed_exceptions=PermissionError, delay=0.25)
def recreate_dir(dir: Path):
    if not str(dir).startswith(r"E:\git\chess-cnn\data"):
        raise Exception("Shouldn't delete just anything: " + str(dir))

    if dir.exists():
        shutil.rmtree(dir)

    dir.mkdir(exist_ok=False)
