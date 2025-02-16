import logging
import os
import pathlib
import random

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

data_raw_path = pathlib.Path(__file__).parent.parent / "data-sets-raw" / "kaggle-images"
target_path = pathlib.Path(__file__).parent.parent / "image-optimizer" / "images"


def main():
    """
    Pick random images from data-sets-raw/kaggle-images and make symlinks to image-optimizer/images
    """
    image_paths = dir_list(data_raw_path)

    picked_images = []
    for path in image_paths:
        picks = random_pick(path, 100)
        picked_images.extend(picks)

    # make symlinks for picked_images to target_path
    for image_path in picked_images:
        log.info("copy %s -> %s", image_path, target_path)
        # shutil.copy(image_path, target_path)
        os.symlink(image_path, target_path / image_path.name)


def random_pick(path: pathlib.Path, n: int):
    files = list(path.glob("*.*"))
    random.shuffle(files)
    return files[:n]


def dir_list(path: pathlib.Path):
    return list(path.glob("*"))


if __name__ == "__main__":
    main()
