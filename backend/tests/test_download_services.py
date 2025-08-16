from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
from backend.services.youtube_download import VideoDownloadService, AudioDownloadService, TranscriptDownloadService
from backend.core.constants import AUDIO_FORMAT, DOWNLOADED_AUDIO_PATH, DOWNLOADED_VIDEO_PATH, LANGUAGE, TRANSCRIPT_OPTION, VIDEO_FORMAT

URL = "https://www.youtube.com/watch?v=test123"


@pytest.mark.parametrize(
    "service_class,expected_format,expected_outtmpl,expected_ext",
    [
        (VideoDownloadService, VIDEO_FORMAT, DOWNLOADED_VIDEO_PATH, 'mp4'),
        (AudioDownloadService, AUDIO_FORMAT, DOWNLOADED_AUDIO_PATH, 'mp3'),
    ]
)
@patch("backend.services.youtube_download.os.path.exists", return_value=True)
@patch("backend.services.youtube_download.YoutubeDL")
def test_download_service(mock_youtubedl, _, service_class, expected_format, expected_outtmpl, expected_ext):
    mock_instance = MagicMock()
    mock_youtubedl.return_value.__enter__.return_value = mock_instance

    # Mock extract_info to return a dummy info dict with requested_downloads
    dummy_info = {
        "requested_downloads": [
            {"filename": f"{expected_outtmpl.replace('%(title)s', 'Test Video').replace('%(ext)s', expected_ext)}"}
        ]
    }
    mock_instance.extract_info.return_value = dummy_info

    service = service_class()
    result = service.download(URL)

    expected_path = dummy_info["requested_downloads"][0]["filename"]
    assert result == expected_path
    mock_youtubedl.assert_called_once_with({
        'format': expected_format,
        'outtmpl': expected_outtmpl,
    })
    mock_instance.extract_info.assert_called_once_with(URL, download=True)


@patch("backend.services.youtube_download.os.path.exists", return_value=True)
@patch("backend.services.youtube_download.YoutubeDL")
def test_transcript_download_service(mock_youtubedl, _):
    mock_instance = mock_youtubedl.return_value.__enter__.return_value

    # Mock the info dict returned by extract_info
    dummy_info = {
        "id": "test123",
        "title": "Test Video",
        "requested_subtitles": {
            LANGUAGE: {"ext": "vtt", "url": "https://example.com/sub.vtt"}
        }
    }
    mock_instance.extract_info.return_value = dummy_info

    service = TranscriptDownloadService()
    result = service.download(URL)

    # Build the expected path
    expected_base = Path(
        mock_instance.prepare_filename.return_value or f"Test Video.mp4").with_suffix("")
    expected_path = str(expected_base.with_suffix(f".{LANGUAGE}.vtt"))

    assert result == expected_path

    # Assert YoutubeDL was instantiated with the correct options
    mock_youtubedl.assert_called_once_with(TRANSCRIPT_OPTION)
    mock_instance.extract_info.assert_called_once_with(URL, download=True)
