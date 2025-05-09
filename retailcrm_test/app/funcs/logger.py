import logging

log_format = "%(asctime)s [%(levelname)s] [%(module)s] - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

logger = logging.getLogger(__name__)
