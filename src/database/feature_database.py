import faiss
import numpy as np
import os
from typing import List, Tuple
from src.utils.logger import logger
from src.config.settings import Settings


class FeatureDatabase:
    def __init__(
        self,
        feature_dim: int,
        database_path: str = Settings.DATABASE_PATH,
        nlist: int = 100,
    ):
        self.feature_dim = feature_dim
        self.database_path = database_path
        self.nlist = nlist
        self.labels = []
        self.labels_path = self.database_path + ".labels"

        if os.path.exists(self.database_path):
            try:
                self.index = faiss.read_index(self.database_path)
                logger.info("Loaded existing FAISS index.")
            except Exception as e:
                logger.error(
                    f"Failed to load FAISS index from {self.database_path}: {e}"
                )
                self.index = self._create_index()
        else:
            self.index = self._create_index()
            logger.info("Initialized new FAISS index.")

        if os.path.exists(self.labels_path):
            try:
                with open(self.labels_path, "r") as f:
                    self.labels = [line.strip() for line in f]
                logger.info(
                    f"Loaded {len(self.labels)} labels from {self.labels_path}."
                )
            except Exception as e:
                logger.error(f"Failed to load labels from {self.labels_path}: {e}")

    def _create_index(self):
        quantizer = faiss.IndexFlatL2(self.feature_dim)
        index = faiss.IndexIVFFlat(quantizer, self.feature_dim, self.nlist)
        index.train(np.zeros((self.nlist, self.feature_dim), dtype=np.float32))
        return index

    def add_features(self, features: np.ndarray, labels: List[str]):
        if features.ndim == 1:
            features = features.reshape(1, -1)
        if features.shape[1] != self.feature_dim:
            logger.error(
                f"Feature dimension mismatch: expected {self.feature_dim}, got {features.shape[1]}"
            )
            return
        self.index.add(features)
        self.labels.extend(labels)
        logger.info(f"Added {features.shape[0]} features to the database.")

    def save_database(self):
        try:
            faiss.write_index(self.index, self.database_path)
            with open(self.labels_path, "w") as f:
                for label in self.labels:
                    f.write(f"{label}\n")
            logger.info(
                f"Saved feature database to {self.database_path} and labels to {self.labels_path}."
            )
        except Exception as e:
            logger.error(f"Failed to save database: {e}")

    def search(
        self, query_features: np.ndarray, k: int = Settings.K_NEIGHBORS
    ) -> Tuple[np.ndarray, np.ndarray]:
        if query_features.shape[1] != self.feature_dim:
            logger.error(
                f"Query feature dimension mismatch: expected {self.feature_dim}, got {query_features.shape[1]}"
            )
            return np.array([]), np.array([])
        distances, indices = self.index.search(query_features, k)
        logger.debug(
            f"Performed search for {query_features.shape[0]} queries with top {k} neighbors."
        )
        return distances, indices
