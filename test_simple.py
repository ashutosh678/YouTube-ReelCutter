import os
import logging
from moviepy.editor import VideoFileClip
import imageio

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    logger.info("Testing imports...")
    try:
        logger.info("MoviePy version: " + str(VideoFileClip.__module__))
        logger.info("ImageIO version: " + str(imageio.__version__))
        logger.info("All imports successful!")
        return True
    except Exception as e:
        logger.error(f"Import test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_imports()
