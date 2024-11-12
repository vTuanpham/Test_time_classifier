import os
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Settings:
    # Class variables (shared across all instances)
    DATA_PATH: ClassVar[str] = os.getenv("DATA_PATH", "./data")
    DATABASE_PATH: ClassVar[str] = os.getenv(
        "DATABASE_PATH", "./database/features.faiss"
    )
    LOGGING_LEVEL: ClassVar[str] = os.getenv("LOGGING_LEVEL", "INFO")
    FEATURE_MODEL: ClassVar[str] = os.getenv("FEATURE_MODEL", "ResNetExtractor")
    K_NEIGHBORS: ClassVar[int] = int(os.getenv("K_NEIGHBORS", 5))
