import os
import logging
from flask import Flask, render_template, request, jsonify, session, send_file
from video_processor import VideoProcessor

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Initialize VideoProcessor
video_processor = VideoProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    try:
        youtube_url = request.form.get('youtube_url')
        if not youtube_url:
            return jsonify({'error': 'No URL provided'}), 400

        if not youtube_url.startswith(('http://www.youtube.com', 'https://www.youtube.com', 'www.youtube.com', 'youtube.com')):
            return jsonify({'error': 'Invalid YouTube URL. Please provide a valid YouTube video URL'}), 400

        # Start processing
        session['processing_url'] = youtube_url
        video_processor.start_processing(youtube_url)

        return jsonify({'status': 'processing', 'message': 'Video processing started'})
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        error_message = str(e)
        if "Private video" in error_message:
            error_message = "This video is private. Please try a public video."
        elif "Video unavailable" in error_message:
            error_message = "This video is unavailable. It might be private, removed, or region-restricted."
        elif "copyright" in error_message.lower():
            error_message = "This video is not accessible due to copyright restrictions."
        else:
            error_message = "Unable to process the video. Please try a different video or check the URL."
        return jsonify({'error': error_message}), 500

@app.route('/status')
def get_status():
    try:
        progress = video_processor.get_progress()
        return jsonify({
            'progress': progress,
            'status': 'completed' if progress >= 100 else 'processing'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<int:segment_id>')
def download_segment(segment_id):
    try:
        file_path = video_processor.get_segment_path(segment_id)
        if not file_path:
            return jsonify({'error': 'Segment not found'}), 404
        return send_file(file_path, mimetype='video/mp4', as_attachment=True)
    except Exception as e:
        logger.error(f"Error downloading segment: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)