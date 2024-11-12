from abc import ABC, abstractmethod
from typing import Union, Tuple, Any
import numpy as np
import torch
from src.utils.helpers import get_device
from src.utils.logger import logger


class FeatureExtractor(ABC):
    def __init__(
        self,
        device: Union[torch.device, None] = None,
    ):
        self.device = device or get_device()
        self.model, self.feature_dim = self.load_model()
        logger.info(
            f"Feature extractor initialized with model: {self.model.__class__.__name__} on device: {self.device}"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.__class__.__name__} with model {self.model.__class__.__name__}"

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        result = self._extract(*args, **kwds)
        # Check type of result
        if not isinstance(result, np.ndarray):
            raise TypeError(
                f"Expected np.ndarray from feature extractor, got {type(result)}"
            )
        return result

    def load_model(self) -> Tuple[Any, int]:
        model, feature_dim = self._load_model()
        if not isinstance(feature_dim, int):
            raise TypeError(
                f"Expected int from feature extractor, got {type(feature_dim)}"
            )
        if feature_dim <= 0:
            raise ValueError(
                f"Feature dimension must be greater than 0, got {feature_dim}"
            )
        if model is None:
            raise ValueError("Model not loaded")
        return model, feature_dim

    @abstractmethod
    def _load_model(self) -> Tuple[Any, int]:
        raise NotImplementedError("Subclasses must implement _load_model")

    @abstractmethod
    def _extract(self, *args: Any, **kwds: Any) -> np.ndarray:
        raise NotImplementedError("Subclasses must implement extract")
