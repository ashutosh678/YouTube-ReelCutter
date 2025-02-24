import os
import logging
from yt_dlp import YoutubeDL
import moviepy.editor as mpy
import numpy as np
from datetime import datetime
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.progress = 0
        self.output_dir = 'temp_videos'
        self.segments = []
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("VideoProcessor initialized")

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            if total_bytes:
                downloaded = d.get('downloaded_bytes', 0)
                self.progress = 10 + int((downloaded / total_bytes) * 20)
                logger.info(f"Download progress: {self.progress}%")

    def start_processing(self, youtube_url):
        try:
            self.progress = 0
            logger.info(f"Starting to process video from URL: {youtube_url}")

            # Configure yt-dlp options
            ydl_opts = {
                'format': 'best[height<=360]',  # Lower quality for better compatibility
                'outtmpl': os.path.join(self.output_dir, 'video_%(id)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'quiet': True,
                'no_warnings': True,
            }

            # Download video using yt-dlp
            with YoutubeDL(ydl_opts) as ydl:
                logger.info("Starting video download with yt-dlp...")
                info = ydl.extract_info(youtube_url, download=True)
                video_path = ydl.prepare_filename(info)

            if not os.path.exists(video_path):
                raise Exception("Video file not found after download")

            self.progress = 30
            logger.info("Processing downloaded video...")

            # Process video into segments
            self._process_video(video_path)

            # Cleanup original video
            try:
                if os.path.exists(video_path):
                    os.remove(video_path)
                    logger.info(f"Cleaned up original video: {video_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup original video: {e}")

        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            # Clean up any partial downloads
            for file in os.listdir(self.output_dir):
                if not file.startswith('segment_'):
                    try:
                        os.remove(os.path.join(self.output_dir, file))
                    except Exception as cleanup_error:
                        logger.warning(f"Cleanup error: {cleanup_error}")
            raise

    def _process_video(self, video_path):
        logger.info(f"Opening video file: {video_path}")
        video_clip = None
        try:
            # Load the video using moviepy's VideoFileClip
            video_clip = mpy.VideoFileClip(video_path)
            logger.info(f"Successfully loaded video: duration={video_clip.duration}s")

            # Calculate number of segments
            segment_duration = min(30.0, video_clip.duration / 10)
            num_segments = min(10, int(video_clip.duration / segment_duration))
            logger.info(f"Planning to create {num_segments} segments of {segment_duration}s each")

            self.segments = []
            for i in range(num_segments):
                try:
                    start_time = i * segment_duration
                    end_time = min((i + 1) * segment_duration, video_clip.duration)
                    logger.info(f"Processing segment {i+1}: {start_time}s to {end_time}s")

                    # Extract the segment using moviepy's subclip method
                    segment = mpy.VideoFileClip(video_path).subclip(t_start=start_time, t_end=end_time)
                    output_path = os.path.join(self.output_dir, f'segment_{i+1}.mp4')

                    # Write segment to file
                    logger.info(f"Writing segment {i+1} to {output_path}")
                    segment.write_videofile(
                        output_path,
                        codec='libx264',
                        audio_codec='aac',
                        temp_audiofile=os.path.join(self.output_dir, f'temp_audio_{i+1}.m4a'),
                        remove_temp=True,
                        logger=None  # Disable moviepy's internal logger
                    )
                    segment.close()  # Close the segment to free up resources
                    self.segments.append(output_path)
                    self.progress = 30 + int((i + 1) / num_segments * 70)
                    logger.info(f"Successfully created segment {i+1}")

                except Exception as e:
                    logger.error(f"Error processing segment {i+1}: {str(e)}")
                    raise

        except Exception as e:
            logger.error(f"Error in video processing: {str(e)}")
            raise
        finally:
            # Ensure the main video clip is closed
            if video_clip is not None:
                try:
                    video_clip.close()
                except:
                    pass

    def get_progress(self):
        return self.progress

    def get_segment_path(self, segment_id):
        if 0 <= segment_id < len(self.segments):
            return self.segments[segment_id]
        return None