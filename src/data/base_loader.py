from abc import ABC, abstractmethod
from typing import List, Tuple, Any
import os
from src.utils.logger import logger


class BaseDataLoader(ABC):
    """Abstract base class for loading data for the classifier."""

    def __init__(self, data_path: str):
        self.data_path = data_path
        if not os.path.isdir(self.data_path):
            logger.error(f"{self.data_path} is not a directory.")
            raise NotADirectoryError(f"{self.data_path} is not a directory.")
        os.makedirs(self.data_path, exist_ok=True)
        self.classes = self._get_classes()
        logger.info(f"Loaded classes: {self.classes}")

    @abstractmethod
    def _get_classes(self) -> List[str]:
        """Return the list of available classes."""

    @abstractmethod
    def load_data(self) -> Tuple[List[Any], List[str]]:
        """Load data and labels from disk."""
