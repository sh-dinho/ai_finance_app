import logging

logger = logging.getLogger("FISPipeline")

def safe_get(d, key, default=None):
    return d[key] if key in d else default
