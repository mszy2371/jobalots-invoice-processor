import logging
import os
from paths import BASE_DIR
from datetime import date

today = date.today()
logger = logging.getLogger("main_logger")
logging_path = os.path.join(BASE_DIR, "app", "logs", f"{today}.log")
logging.basicConfig(
    filename=logging_path,
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)

