import os
from moviepy.editor import VideoFileClip
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_moviepy_installation():
    logger.info("Testing MoviePy installation...")
    try:
        # Create a blank video clip (this doesn't require any actual video file)
        clip = VideoFileClip
        logger.info("MoviePy VideoFileClip class is available")
        logger.info("MoviePy installation test successful!")
        return True
    except Exception as e:
        logger.error(f"MoviePy test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_moviepy_installation()
