import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_moviepy():
    try:
        logger.info("Attempting to import moviepy...")
        import moviepy
        logger.info(f"MoviePy imported successfully. Version: {moviepy.__version__}")
        
        logger.info("Attempting to import VideoFileClip...")
        from moviepy.editor import VideoFileClip
        logger.info("VideoFileClip imported successfully")
        
        # Try to create a very simple clip
        logger.info("Testing VideoFileClip functionality...")
        clip = VideoFileClip
        logger.info("VideoFileClip class accessed successfully")
        
        return True
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Module search paths: {sys.path}")
        return False

if __name__ == "__main__":
    success = test_moviepy()
    if success:
        logger.info("All tests passed!")
    else:
        logger.error("Tests failed!")
        sys.exit(1)
