from yt_dlp import YoutubeDL
from backend.core.constants import AUDIO_OPTION, DOWNLOADED_TRANSCRIPT_PATH, LANGUAGE, TRANSCRIPT_EXT, VIDEO_OPTION
from youtube_transcript_api import YouTubeTranscriptApi

import os
import json
import re
from pathlib import Path


class BaseDownloadService:
    def _download(self, video_url: str, ydl_opts: dict, path_extractor) -> Path:
        """
        Base method to download content from a URL.

        :param video_url: The URL of the content to download.
        :return: The file path where the content is saved.
        """

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            output_path = path_extractor(info, ydl)

        if not os.path.exists(output_path):
            raise FileNotFoundError(f"File '{output_path}' does not exist.")

    def _sanitize_filename(self, name: str) -> str:
        # Remove or replace invalid characters
        return re.sub(r'[\\/*?:"<>|]', "_", name)


class VideoDownloadService(BaseDownloadService):
    def download(self, video_url: str) -> Path:
        """
        Downloads a video from the given URL and returns the file path.

        :param video_url: The URL of the video to download.
        :return: The file path where the video is saved.
        """
        return self._download(video_url, VIDEO_OPTION, lambda info, ydl: info["requested_downloads"][0]["filename"])


class AudioDownloadService(BaseDownloadService):
    def download(self, video_url: str) -> Path:
        """
        Downloads the audio from the given video URL and returns the file path.

        :param video_url: The URL of the video to extract audio from.
        :return: The file path where the audio is saved.
        """
        return self._download(video_url, AUDIO_OPTION, lambda info, ydl: info["requested_downloads"][0]["filename"])


class TranscriptDownloadService(BaseDownloadService):
    def download(self, video_url: str) -> Path:
        """
        Downloads the transcript of the video from the given URL.

        :param video_url: The URL of the video to download the transcript from.
        :return: The file path where the transcript is saved.
        """
        video_id = video_url.rsplit('v=', 1)[-1]

        # Create an instance
        ytt_api = YouTubeTranscriptApi()

        # Fetch transcript, languages in priority order
        transcript = ytt_api.fetch(
            video_id, languages=LANGUAGE, preserve_formatting=False)

        with YoutubeDL({}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info["title"]
            title = self._sanitize_filename(title)

        output_path = DOWNLOADED_TRANSCRIPT_PATH % {
            "title": title, "ext": TRANSCRIPT_EXT}
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transcript.to_raw_data(), f,
                      ensure_ascii=False, indent=2)

        return output_path


# Example usage
if __name__ == "__main__":
    video_service = VideoDownloadService()
    audio_service = AudioDownloadService()
    transcript_service = TranscriptDownloadService()

    video_url = "https://www.youtube.com/watch?v=-MRIkiCRVW8"

    # video_path = video_service.download(video_url)
    # print(f"Video downloaded to: {video_path}")

    # audio_path = audio_service.download(video_url)
    # print(f"Audio downloaded to: {audio_path}")

    transcript_path = transcript_service.download(video_url)
    print(f"Transcript downloaded to: {transcript_path}")
