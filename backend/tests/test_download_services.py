from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
from backend.services.youtube_download import VideoDownloadService, AudioDownloadService, TranscriptDownloadService
from backend.core.constants import AUDIO_FORMAT, DOWNLOADED_AUDIO_PATH, DOWNLOADED_TRANSCRIPT_PATH, DOWNLOADED_VIDEO_PATH, TRANSCRIPT_EXT, VIDEO_FORMAT

URL = "https://www.youtube.com/watch?v=test123"
TITLE = "Fake / title"


@pytest.mark.parametrize(
    "service_class,expected_format,expected_outtmpl,expected_ext",
    [
        (VideoDownloadService, VIDEO_FORMAT, DOWNLOADED_VIDEO_PATH, 'mp4'),
        (AudioDownloadService, AUDIO_FORMAT, DOWNLOADED_AUDIO_PATH, 'mp3'),
    ]
)
@patch("backend.services.youtube_download.os.rename", return_value=None)
@patch("backend.services.youtube_download.os.path.exists", return_value=True)
@patch("backend.services.youtube_download.YoutubeDL")
def test_download_service(mock_youtubedl, _, mock_rename, service_class, expected_format, expected_outtmpl, expected_ext):
    service = service_class()

    mock_instance = MagicMock()
    mock_youtubedl.return_value.__enter__.return_value = mock_instance

    sanitized_title = "Fake _ title"
    # Mock extract_info to return a dummy info dict with requested_downloads
    dummy_info = {
        "title": sanitized_title,
        "ext": expected_ext,
        "requested_downloads": [
            {"filename": f"{expected_outtmpl.replace('%(title)s', sanitized_title).replace('%(ext)s', expected_ext)}"}
        ]
    }
    mock_instance.extract_info.return_value = dummy_info

    result = service.download(URL)

    expected_path = dummy_info["requested_downloads"][0]["filename"]
    assert result == expected_path
    mock_youtubedl.assert_called_once_with({
        'format': expected_format,
        'outtmpl': expected_outtmpl,
    })
    mock_instance.extract_info.assert_called_once_with(URL, download=True)


@patch("backend.services.youtube_download.YouTubeTranscriptApi")
@patch("backend.services.youtube_download.YoutubeDL")
def test_transcript_download_service(mock_youtubedl, mock_youtube_transcript_api):
    service = TranscriptDownloadService()

    sanitized_title = "Fake _ title"
    fake_transcript_data = {"text": "hello world"}

    mock_youtubedl.return_value.__enter__.return_value.extract_info.return_value = {
        "title": sanitized_title}
    mock_youtube_transcript_api.return_value.fetch.return_value.to_raw_data.return_value = fake_transcript_data

    result = service.download(URL)

    # Build the expected path
    expected_path = DOWNLOADED_TRANSCRIPT_PATH % {
        "title": sanitized_title, "ext": TRANSCRIPT_EXT}

    assert result == expected_path
