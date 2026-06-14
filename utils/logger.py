"""
Logger Utility
"""
import logging
import os
from config import LOG_FILE

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE, encoding='utf-8'), logging.StreamHandler()]
)
logger = logging.getLogger("AI-Model-Firewall")

def log_info(msg): logger.info(msg)
def log_warning(msg): logger.warning(msg)
def log_error(msg): logger.error(msg)

def log_scan_result(file_path, module_name, success, message):
    status = "PASS" if success else "FAIL"
    logger.info(f"[{status}] {module_name} | {os.path.basename(file_path)} | {message}")