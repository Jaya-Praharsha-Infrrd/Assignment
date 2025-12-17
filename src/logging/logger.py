import logging
from typing import Optional


class LoggerSingleton:
    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls, name: str = "app") -> logging.Logger:
        if cls._instance is not None:
            return cls._instance

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.propagate = False

        cls._instance = logger
        return logger
