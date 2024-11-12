import importlib
from PIL import Image, UnidentifiedImageError
import torch
from src.utils.logger import logger


def dynamic_import(module_name, class_name):
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls


def load_image(image_path):
    try:
        return Image.open(image_path).convert("RGB")
    except UnidentifiedImageError:
        logger.error(f"Cannot identify image file {image_path}.")
        return None
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {e}")
        return None


def is_image_file(filename):
    return any(
        filename.lower().endswith(ext)
        for ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]
    )


def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")
