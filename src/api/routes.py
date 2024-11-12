import os
from typing import List
import shutil
import uuid
from fastapi import File, UploadFile, Form, HTTPException, APIRouter
import numpy as np

from src.config.settings import Settings
from src.data.data_loader import DataLoader
from src.database.feature_database import FeatureDatabase
from src.search.similarity_search import SimilaritySearch
from src.classifier.classifier import Classifier
from src.utils.logger import logger
from src.utils.helpers import load_image, dynamic_import


class TestTimeRouter:
    def __init__(self):
        self.router = APIRouter()
        self._setup_routes()

    @staticmethod
    def startup_event():
        global data_loader, feature_extractor, feature_db, similarity_search, classifier

        logger.info("Initializing Test-Time Compute Classifier API components.")

        data_loader = DataLoader(Settings.DATA_PATH)

        try:
            feature_extractor = dynamic_import("src.features", Settings.FEATURE_MODEL)()
        except Exception as e:
            logger.error(f"Failed to load feature extractor: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load feature extractor."
            )
        feature_db = FeatureDatabase(feature_dim=feature_extractor.feature_dim)
        similarity_search = SimilaritySearch(feature_db)
        classifier = Classifier(similarity_search)

        # Check database file is missing
        if not os.path.exists(Settings.DATABASE_PATH):
            logger.info(
                f"Data directory found at: {Settings.DATA_PATH}, creating feature database."
            )

            # Load data from Dataloader
            image_paths, labels = data_loader.load_data()

            # Trigger preprocessing to extract features and update the database
            try:
                feature_vectors = []
                valid_labels = []
                for image, label in zip(image_paths, labels):
                    if image is not None:
                        feat = feature_extractor(image)
                        if feat.size > 0:
                            feature_vectors.append(feat)
                            valid_labels.append(label)
                        else:
                            logger.warning(
                                "Feature extraction failed for an uploaded image."
                            )
                if feature_vectors:
                    features_np = np.array(feature_vectors).astype("float32")
                    feature_db.add_features(features_np, valid_labels)
                    feature_db.save_database()
                    logger.info("Uploaded images processed and database updated.")
                else:
                    logger.warning("No valid features extracted from uploaded images.")
            except Exception as e:
                logger.error(
                    f"Failed during feature extraction and database update: {e}"
                )
                raise HTTPException(
                    status_code=500, detail="Failed to process uploaded images."
                )

        logger.info("API components initialized successfully.")

    def _setup_routes(self):
        """Set up routes for the Test-Time Compute Classifier API."""
        self.router.get("/", summary="API index", description="API index endpoint.")(
            self.index
        )
        self.router.post("/add_class", summary="Add class")(self.add_class)
        self.router.post("/upload_images", summary="Upload images")(self.upload_images)
        self.router.post("/classify", summary="Classify image")(self.classify_image)
        self.router.get("/classes", summary="List classes")(self.list_classes)
        self.router.get("/health", summary="Health check")(self.health_check)

    def index(self):
        return {"message": "Test-Time Compute Classifier API is running."}

    async def add_class(self, class_name: str = Form(...)):
        class_dir = os.path.join(Settings.DATA_PATH, class_name)
        if os.path.exists(class_dir):
            logger.warning(f"Class '{class_name}' already exists.")
            raise HTTPException(
                status_code=400, detail=f"Class '{class_name}' already exists."
            )
        try:
            os.makedirs(class_dir, exist_ok=False)
            logger.info(f"Created new class directory: {class_dir}")
            return {"message": f"Class '{class_name}' created successfully."}
        except Exception as e:
            logger.error(f"Failed to create class '{class_name}': {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error.")

    async def upload_images(
        self, class_name: str = Form(...), files: List[UploadFile] = File(...)
    ):
        class_dir = os.path.join(Settings.DATA_PATH, class_name)
        if not os.path.exists(class_dir):
            logger.warning(f"Class '{class_name}' does not exist.")
            raise HTTPException(
                status_code=404, detail=f"Class '{class_name}' does not exist."
            )

        saved_files = []
        for file in files:
            # Generate a unique filename to prevent overwriting
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"
            file_path = os.path.join(class_dir, unique_filename)
            try:
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                saved_files.append(unique_filename)
                logger.info(f"Saved image {unique_filename} to class '{class_name}'.")
            except Exception as e:
                logger.error(f"Failed to save image '{file.filename}': {e}")
                raise HTTPException(
                    status_code=500, detail=f"Failed to save image '{file.filename}'."
                )
            finally:
                file.file.close()

        # Trigger preprocessing to extract features and update the database
        try:
            image_objects = [
                load_image(os.path.join(class_dir, fname)) for fname in saved_files
            ]
            feature_vectors = []
            valid_labels = []
            for image in image_objects:
                if image is not None:
                    feat = feature_extractor.extract(image)
                    if feat.size > 0:
                        feature_vectors.append(feat)
                        valid_labels.append(class_name)
                    else:
                        logger.warning(
                            "Feature extraction failed for an uploaded image."
                        )
            if feature_vectors:
                features_np = np.array(feature_vectors).astype("float32")
                feature_db.add_features(features_np, valid_labels)
                feature_db.save_database()
                logger.info("Uploaded images processed and database updated.")
            else:
                logger.warning("No valid features extracted from uploaded images.")
        except Exception as e:
            logger.error(f"Failed during feature extraction and database update: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to process uploaded images."
            )

        return {
            "message": f"Uploaded {len(saved_files)} images to class '{class_name}' successfully."
        }

    async def classify_image(self, file: UploadFile = File(...)):
        # Save the uploaded image to a temporary location
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_filename = f"{uuid.uuid4().hex}_{file.filename}"
        temp_path = os.path.join(temp_dir, temp_filename)
        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info(f"Saved uploaded image to temporary path: {temp_path}")
        except Exception as e:
            logger.error(f"Failed to save uploaded image: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to save uploaded image."
            )
        finally:
            file.file.close()

        # Load and process the image
        image = load_image(temp_path)
        if image is None:
            shutil.rmtree(temp_dir)
            logger.error("Failed to load the uploaded image.")
            raise HTTPException(status_code=400, detail="Invalid image file.")

        # Extract features
        try:
            feature_vector = feature_extractor(image)
            if feature_vector.size == 0:
                shutil.rmtree(temp_dir)
                logger.error("Feature extraction returned empty vector.")
                raise HTTPException(
                    status_code=500, detail="Failed to extract features from the image."
                )
            feature_np = feature_vector.reshape(1, -1).astype("float32")
            # Perform classification
            prediction = classifier.predict(feature_np, Settings.K_NEIGHBORS)
            logger.info(f"Image classified as: {prediction}")
        except Exception as e:
            logger.error(f"Failed during classification: {e}")
            shutil.rmtree(temp_dir)
            raise HTTPException(status_code=500, detail="Failed to classify the image.")

        # Clean up temporary files
        shutil.rmtree(temp_dir)

        return {"prediction": prediction}

    async def list_classes(self):
        classes = data_loader.classes
        return {"classes": classes}

    async def health_check(self):
        return {"status": "API is running successfully."}
