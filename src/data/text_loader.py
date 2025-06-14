import os
from typing import List, Tuple
from src.utils.logger import logger
from .base_loader import BaseDataLoader


class TextDataLoader(BaseDataLoader):
    """Load text documents organized in class subdirectories."""

    def __init__(self, data_path: str):
        super().__init__(data_path)

    def _get_classes(self) -> List[str]:
        classes = [d for d in os.listdir(self.data_path) if os.path.isdir(os.path.join(self.data_path, d))]
        if not classes:
            logger.warning(f"No class directories found in {self.data_path}.")
        return classes

    def load_data(self) -> Tuple[List[str], List[str]]:
        texts = []
        labels = []
        for label in self.classes:
            class_dir = os.path.join(self.data_path, label)
            if not os.path.isdir(class_dir):
                logger.warning(f"{class_dir} is not a directory. Skipping.")
                continue
            for file in os.listdir(class_dir):
                file_path = os.path.join(class_dir, file)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            texts.append(f.read())
                        labels.append(label)
                    except Exception as e:
                        logger.error(f"Error reading {file_path}: {e}")
        logger.info(f"Loaded {len(texts)} text documents from {self.data_path}.")
        return texts, labels
