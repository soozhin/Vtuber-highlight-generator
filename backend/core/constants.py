# Transcript chunk size in seconds
TRANSCRIPT_CHUNK_SIZE = 60

# These paths are used to store downloaded videos and audios.
DOWNLOADED_VIDEO_DIR = "./backend/download/downloaded_videos"
DOWNLOADED_AUDIO_DIR = "./backend/download/downloaded_audios"
DOWNLOADED_TRANSCRIPT_DIR = "./backend/download/downloaded_transcripts"
DOWNLOADED_VIDEO_PATH = f"{DOWNLOADED_VIDEO_DIR}/%(title)s.%(ext)s"
DOWNLOADED_AUDIO_PATH = f"{DOWNLOADED_AUDIO_DIR}/%(title)s.%(ext)s"
DOWNLOADED_TRANSCRIPT_PATH = f"{DOWNLOADED_TRANSCRIPT_DIR}/%(title)s.%(ext)s"

# Constants for video and audio formats
VIDEO_FORMAT = 'bestvideo+bestaudio/best/mp4'
AUDIO_FORMAT = 'mp3/bestaudio'
LANGUAGE = 'ja'  # Default language for transcription

VIDEO_OPTION = {
    'format': VIDEO_FORMAT,
    'outtmpl': DOWNLOADED_VIDEO_PATH,
}

AUDIO_OPTION = {
    'format': AUDIO_FORMAT,
    'outtmpl': DOWNLOADED_AUDIO_PATH,
}

TRANSCRIPT_OPTION = {
    'writesubtitles': True,
    'subtitleslangs': ['ja'],  # Japanese subtitles
    'outtmpl': DOWNLOADED_TRANSCRIPT_PATH,
    'skip_download': True,  # Skip downloading the video
    'writeautomaticsub': True,  # Download automatic subtitles if available
    'subtitlesformat': 'vtt',  # Use VTT format for subtitles
}
