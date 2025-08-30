# Transcript chunk size in seconds
TRANSCRIPT_CHUNK_SIZE = 60

# Transcript scores
MAX_SCORE = 10
MIN_SCORE = 0
THRESHOLD_SCORE = 7

# AI request
AI_REQUEST_PER_MINUTE_LIMIT = 15
AI_REQUEST_BUFFER_SECONDS = 10
SLEEP_TIME_BEFORE_RETRY_SECONDS = 1

# Highlight
START = "start"
END = "end"
TEXT = "text"
HIGHLIGHT_SCORE = "highlight_score"
REASON = "reason"
DURATION = "duration"

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
LANGUAGE = ['ja', 'en']  # Default language for transcription
TRANSCRIPT_EXT = "json"

VIDEO_OPTION = {
    'format': VIDEO_FORMAT,
    'outtmpl': DOWNLOADED_VIDEO_PATH,
}

AUDIO_OPTION = {
    'format': AUDIO_FORMAT,
    'outtmpl': DOWNLOADED_AUDIO_PATH,
}

# AI
AI_RESPONSE_PRECEDING_STRING_FORMAT = r"^```(?:json)?\s*"
AI_RESPONSE_SUCCEDING_STRING_FORMAT = r"\s*```$"
HIGHLIGHT_DETECTION_PROMPT = f"""
You are a livestream highlight detector.

Highlight definition:
- Emotional reactions (laughing, excitement, sarcasm, angry outbursts)
- Audience interactions (reading comments)
- Funny or surprising statements (cute moments)
- Interesting discussions (personal stories, insights, or opinions)

Transcript chunk:
\"\"\"%s\"\"\"

Return a JSON object with:
- highlight_score ({MIN_SCORE}-{MAX_SCORE}, {MIN_SCORE} = not highlight, {MAX_SCORE} = very strong)
- reason (short explanation)
"""
