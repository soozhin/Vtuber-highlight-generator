from yt_dlp import YoutubeDL
from backend.core.constants import AUDIO_OPTION, LANGUAGE, TRANSCRIPT_OPTION, VIDEO_OPTION

import os
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

        return output_path


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
        return self._download(video_url, TRANSCRIPT_OPTION, lambda info,
                              ydl: self._transcript_path_extractor(info, ydl))

    def _transcript_path_extractor(self, info, ydl):
        base_filename = Path(ydl.prepare_filename(
            info)).with_suffix("")  # remove .mp4
        subtitles = info.get("requested_subtitles")

        if not subtitles or LANGUAGE not in subtitles:
            raise ValueError(f"No subtitles found for language '{LANGUAGE}'")

        ext = subtitles[LANGUAGE].get("ext", "vtt")
        return str(base_filename.with_suffix(f".{LANGUAGE}.{ext}"))


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
