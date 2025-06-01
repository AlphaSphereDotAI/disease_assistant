from datetime import datetime
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

DEBUG: bool = getenv(key="DEBUG", default="True").lower() == "true"
SERVER_NAME: str = getenv(key="GRADIO_SERVER_NAME", default="localhost")
SERVER_PORT: int = int(getenv(key="GRADIO_SERVER_PORT", default="8080"))
CURRENT_DATE: str = datetime.now().strftime(format="%Y-%m-%d_%H-%M-%S")

BASE_DIR: Path = Path.cwd()
RESULTS_DIR: Path = BASE_DIR / "results"
LOG_DIR: Path = BASE_DIR / "logs"

RESULTS_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

logger.add(
    sink=LOG_DIR / f"{CURRENT_DATE}.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    colorize=True,
)
logger.info(f"Current date: {CURRENT_DATE}")
logger.info(f"Base directory: {BASE_DIR}")
logger.info(f"Results directory: {RESULTS_DIR}")
logger.info(f"Log directory: {LOG_DIR}")
