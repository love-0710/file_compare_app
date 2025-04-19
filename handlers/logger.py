import logging
import os
from datetime import datetime

# Setup logging configuration
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"comparison_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def log_starting_comparison(before_file, after_file):
    logging.info(f"Starting comparison between '{before_file}' and '{after_file}'")

def log_comparison_result(summary: str):
    logging.info(summary)
