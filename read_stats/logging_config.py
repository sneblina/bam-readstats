import logging
import os

def setup_logger(name, log_dir="log", log_file='bamreadstats', level=logging.INFO):
    """
    Set up and return a logger that writes to a specific log file inside log_dir.

    Args:
        name (str): Logger name (usually __name__ from the module).
        log_dir (str): Directory where log files are stored.
        log_file (str): Log file name; if None, uses '{name}.log'.
        level (int): Logging level.

    Returns:
        logging.Logger: Configured logger instance.
    """
    os.makedirs(log_dir, exist_ok=True)

    log_file = f"{log_file}.log"

    log_path = os.path.join(log_dir, log_file)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers for this logger to prevent duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Important: Disable propagation to avoid printing logs to the root logger (and console)
    logger.propagate = False

    return logger
