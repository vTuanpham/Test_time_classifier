from typing import Union
from PIL import Image
import numpy as np
import torch
from torchvision import models, transforms
from .feature_extractor import FeatureExtractor
from src.utils.logger import logger


class ResNetExtractor(FeatureExtractor):
    def __init__(
        self,
        device: Union[torch.device, None] = None,
    ):
        super().__init__(device)
        self.transform = self._get_transform()
        self.model.eval()

    def _load_model(self):
        model = getattr(models, "resnet50")(pretrained=True)
        feature_dim = model.fc.in_features
        model = torch.nn.Sequential(*list(model.children())[:-1])
        model.to(self.device)

        return model, feature_dim

    def _get_transform(self):
        return transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )

    def _extract(self, image: Union[Image.Image, str, None]) -> np.ndarray:
        if image is None:
            logger.error("Received None image for feature extraction.")
            return np.array([])
        elif isinstance(image, str):
            try:
                image = Image.open(image).convert("RGB")
            except Exception as e:
                logger.error(f"Error loading image {image}: {e}")
                return np.array([])
        with torch.no_grad():
            image = self.transform(image).unsqueeze(0).to(self.device)
            features = self.model(image)
            features = features.cpu().numpy().flatten()
        return features

