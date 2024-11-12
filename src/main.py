import argparse
import numpy as np

from src.config.settings import Settings
from src.data.data_loader import DataLoader
from src.features.feature_extractor import FeatureExtractor
from src.database.feature_database import FeatureDatabase
from src.search.similarity_search import SimilaritySearch
from src.classifier.classifier import Classifier
from src.utils.logger import logger
from src.utils.helpers import load_image


def parse_args():
    parser = argparse.ArgumentParser(description="Test-Time Compute Classifier")
    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        choices=["preprocess", "classify"],
        help="Operation mode: preprocess or classify.",
    )
    parser.add_argument(
        "--data_path", type=str, default=Settings.DATA_PATH, help="Path to the dataset."
    )
    parser.add_argument(
        "--input", type=str, help="Path to input image for classification."
    )
    parser.add_argument(
        "--k",
        type=int,
        default=Settings.K_NEIGHBORS,
        help="Number of neighbors to consider.",
    )
    return parser.parse_args()


def preprocess(data_path: str = Settings.DATA_PATH):
    data_loader = DataLoader(data_path)
    image_paths, labels = data_loader.load_data()

    extractor = FeatureExtractor()
    features = []
    valid_labels = []
    for path, label in zip(image_paths, labels):
        image = load_image(path)
        if image is not None:
            feat = extractor.extract(image)
            if feat.size > 0:
                features.append(feat)
                valid_labels.append(label)
            else:
                logger.warning(f"Feature extraction failed for {path}.")
        else:
            logger.warning(f"Image loading failed for {path}. Skipping.")
    if not features:
        logger.error("No features extracted. Exiting preprocessing.")
        return
    features = np.array(features).astype("float32")

    db = FeatureDatabase(feature_dim=Settings.FEATURE_DIMENSION)
    db.add_features(features, valid_labels)
    db.save_database()


def classify(input_path: str, k: int = Settings.K_NEIGHBORS):
    db = FeatureDatabase(feature_dim=Settings.FEATURE_DIMENSION)
    search = SimilaritySearch(db)
    classifier = Classifier(search)

    extractor = FeatureExtractor()
    image = load_image(input_path)
    if image is None:
        logger.error(f"Failed to load input image: {input_path}")
        return
    feat = extractor.extract(image)
    if feat.size == 0:
        logger.error("Feature extraction returned empty features.")
        return
    feat = feat.reshape(1, -1).astype("float32")

    prediction = classifier.predict(feat, k)
    logger.info(f"Classification result: {prediction}")


def main():
    args = parse_args()
    if args.mode == "preprocess":
        preprocess(data_path=args.data_path)
    elif args.mode == "classify":
        if not args.input:
            logger.error("Input image path is required for classification.")
            return
        classify(args.input, args.k)


if __name__ == "__main__":
    main()
