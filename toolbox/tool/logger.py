import logging
import sys


def _get_logging_level():
    if '--verbose' in sys.argv:
        return logging.DEBUG
    return logging.INFO

logger = logging.Logger('app', level=_get_logging_level())
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(_get_logging_level())
handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(handler)
