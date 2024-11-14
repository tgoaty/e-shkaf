# logger_config.py
import logging
from logging.handlers import RotatingFileHandler


def get_logger(name: str, log_file: str = "app.log", max_size: int = 5 * 1024 * 1024, backup_count: int = 1):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Проверяем, если у логгера уже есть обработчики, не добавляем новые
    if not logger.hasHandlers():
        # Обработчик для записи в файл с ротацией
        file_handler = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count, encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Обработчик для вывода логов в консоль
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        logger.debug(f"Logger initialized for {name} with file {log_file}")
    else:
        logger.debug(f"Logger for {name} already initialized")

    return logger
