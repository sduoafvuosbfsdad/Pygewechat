import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s')

logger = logging.getLogger(__name__)
logger.debug('debugging')