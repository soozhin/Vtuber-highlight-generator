import pytest
from unittest.mock import patch, MagicMock
from backend.services.youtube_download import VideoDownloadService, AudioDownloadService
from backend.core.constants import AUDIO_FORMAT, DOWNLOADED_VIDEO_PATH, DOWNLOADED_AUDIO_PATH, VIDEO_FORMAT

@pytest.mark.parametrize(
    "service_class,expected_format,expected_path",
    [
        (VideoDownloadService, VIDEO_FORMAT, f"{DOWNLOADED_VIDEO_PATH}/%(title)s.%(ext)s"),
        (AudioDownloadService, AUDIO_FORMAT, f"{DOWNLOADED_AUDIO_PATH}/%(title)s.%(ext)s"),
    ]
)
@patch("backend.services.youtube_download.YoutubeDL")
def test_download_service(mock_youtubedl, service_class, expected_format, expected_path):
    mock_instance = MagicMock()
    mock_youtubedl.return_value.__enter__.return_value = mock_instance

    service = service_class()
    url = "https://www.youtube.com/watch?v=test123"
    result = service.download(url)

    assert result == expected_path
    mock_youtubedl.assert_called_once_with({
        'format': expected_format,
        'outtmpl': expected_path,
    })
    mock_instance.download.assert_called_once_with([url])
