import sys
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def check_environment():
    logger.info("Python version: " + sys.version)
    logger.info("Python executable: " + sys.executable)
    logger.info("Python path:")
    for path in sys.path:
        logger.info("  - " + path)
    
    try:
        import pkg_resources
        logger.info("\nInstalled packages:")
        for package in pkg_resources.working_set:
            logger.info(f"  - {package.key} ({package.version})")
    except ImportError:
        logger.error("Could not import pkg_resources")

    try:
        import moviepy
        logger.info("\nMoviePy found!")
        logger.info(f"MoviePy path: {moviepy.__file__}")
        logger.info(f"MoviePy version: {moviepy.__version__}")
    except ImportError as e:
        logger.error(f"MoviePy import error: {e}")

if __name__ == "__main__":
    check_environment()
