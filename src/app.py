from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.logger import logger
from src.api.routes import TestTimeRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Test-Time Compute Classifier API.")

    logger.info("Entering startup event.")
    TestTimeRouter.startup_event()
    logger.info("Startup event completed.")

    logger.info("Test-Time Compute Classifier App is running.")

    yield

    logger.info("Stopping Test-Time Compute Classifier API.")


app = FastAPI(
    title="Test-Time Compute Classifier API",
    description="API for managing classes, uploading images, and classifying new examples using similarity search.",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
origins = [
    "http://localhost:3000",  # React frontend
    # Add other origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

test_time_router = TestTimeRouter()
app.include_router(test_time_router.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(f"{Path(__file__).stem}:app", host="0.0.0.0", port=8000, reload=True)
