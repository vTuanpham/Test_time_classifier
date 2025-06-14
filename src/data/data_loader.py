import os
from typing import List, Tuple
from src.utils.helpers import is_image_file
from src.utils.logger import logger
from .base_loader import BaseDataLoader


class ImageDataLoader(BaseDataLoader):
    """Load images organized in class subdirectories."""

    def __init__(self, data_path: str):
        logger.info(f"Data path: {data_path}")
        super().__init__(data_path)

    def _get_classes(self) -> List[str]:
        classes = [
            d
            for d in os.listdir(self.data_path)
            if os.path.isdir(os.path.join(self.data_path, d))
        ]
        if not classes:
            logger.warning(f"No class directories found in {self.data_path}.")
        return classes

    def load_data(self) -> Tuple[List[str], List[str]]:
        image_paths = []
        labels = []
        for label in self.classes:
            class_dir = os.path.join(self.data_path, label)
            if not os.path.isdir(class_dir):
                logger.warning(f"{class_dir} is not a directory. Skipping.")
                continue
            for file in os.listdir(class_dir):
                if is_image_file(file):
                    image_path = os.path.join(class_dir, file)
                    image_paths.append(image_path)
                    labels.append(label)
                else:
                    logger.debug(f"Non-image file skipped: {file}")
        logger.info(f"Loaded {len(image_paths)} images from {self.data_path}.")
        return image_paths, labels


# Backwards compatibility
DataLoader = ImageDataLoader
