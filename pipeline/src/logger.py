from loguru import logger
import os

# Создаём папку для логов, если её нет
LOG_DIR = "/opt/airflow/src/app-logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Основной файл логов
LOG_FILE = os.path.join(LOG_DIR, "app.log")


logger.remove()
logger.add(
    LOG_FILE,
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    level="DEBUG"
)


logger.add(
    lambda msg: print(msg, end=""),
    colorize=True,
    level="INFO"
)