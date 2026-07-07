import logging
import os


def setup_logger():

    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("employee_system")

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(
        "logs/run.log",
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
if __name__ == "__main__":
    logger = setup_logger()
    logger.info("程序启动")
    print("日志创建成功")