from fastapi import FastAPI
import logging
import os
from fastapi.middleware.cors import CORSMiddleware
from aiocache import caches, cached
from aiocache.serializers import PickleSerializer

log_level = os.environ.get("LOG_LEVEL", "ERROR").upper()

# Configure the logging
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
_MB = 1024**2
MAX_REQUEST_SIZE_IN_MB = int(os.environ.get("MAX_REQUEST_SIZE_IN_MB", "25")) * _MB
app = FastAPI(max_request_body_size=MAX_REQUEST_SIZE_IN_MB)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

EMBEDDING_ENABLED = os.environ.get("EMBEDDING_ENABLED", "false").lower().strip()
EMBEDDING_ENABLED = EMBEDDING_ENABLED not in ["0", "false", "no"]
logger.info(f"Embedding Enabled: {EMBEDDING_ENABLED}")

TRANSCRIPTION_ENABLED = os.environ.get("TRANSCRIPTION_ENABLED", "false").lower().strip()
TRANSCRIPTION_ENABLED = TRANSCRIPTION_ENABLED not in ["0", "false", "no"]
logger.info(f"Speech to Text Enabled: {TRANSCRIPTION_ENABLED}")

PLATFORM_ENABLED = os.environ.get("STRAICO_PLATFORM_ACCESS_TOKEN") is not None
logger.info(f"Platform Enabled: {PLATFORM_ENABLED}")

TTS_PROVIDER_STRAICO_PLATFORM = "STRAICO_PLATFORM"
TTS_PROVIDER_LAZYBIRD = "LAZYBIRD"
TTS_PROVIDER = os.environ.get("TTS_PROVIDER", TTS_PROVIDER_STRAICO_PLATFORM)

TIMEOUT = int(os.environ.get("STRAICO_TIMEOUT", "600"))

# Cache Configuration
CACHE_TTL = int(os.environ.get("CACHE_TTL", "600"))  # Default to 10 minutes
logger.info(f"Cache TTL set to: {CACHE_TTL} seconds")

caches.set_config(
    {
        "default": {
            "cache": "aiocache.SimpleMemoryCache",
            "serializer": {"class": "aiocache.serializers.PickleSerializer"},
            "ttl": CACHE_TTL,
        }
    }
)

app.cached = cached
