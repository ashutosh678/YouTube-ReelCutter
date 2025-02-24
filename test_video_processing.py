import os
import logging
from moviepy.editor import VideoFileClip
from yt_dlp import YoutubeDL

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_video_processing():
    try:
        # Test video URL (use a short video)
        test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # First YouTube video ever
        output_dir = 'temp_videos'
        os.makedirs(output_dir, exist_ok=True)

        # Download video
        logger.info("Starting video download...")
        ydl_opts = {
            'format': 'best[height<=360]',
            'outtmpl': os.path.join(output_dir, 'test_video.mp4'),
            'quiet': True
        }

        with YoutubeDL(ydl_opts) as ydl:
            logger.info("Downloading video...")
            ydl.download([test_url])
            video_path = os.path.join(output_dir, 'test_video.mp4')

        # Test VideoFileClip functionality
        logger.info(f"Testing VideoFileClip with file: {video_path}")
        with VideoFileClip(video_path) as video:
            logger.info(f"Successfully loaded video. Duration: {video.duration}s")
            
            # Try to create a short subclip
            logger.info("Attempting to create subclip...")
            clip = video.subclip(0, min(5, video.duration))
            
            output_path = os.path.join(output_dir, 'test_segment.mp4')
            logger.info(f"Writing test segment to: {output_path}")
            
            clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp_audio.m4a',
                remove_temp=True,
                logger=None
            )
            logger.info("Successfully created test segment")

        return True
    except Exception as e:
        logger.error(f"Error in test: {str(e)}")
        return False

if __name__ == "__main__":
    test_video_processing()
