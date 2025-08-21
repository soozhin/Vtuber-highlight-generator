from unittest.mock import call
from backend.services.video_clipping import VideoClippingService
from backend.core.constants import START, END
from unittest.mock import patch


@patch("backend.services.video_clipping.ffmpeg")
def test_video_clipping_service(mock_ffmpeg):
    """
    Test the VideoClippingService with a sample video and highlights.
    """
    mock_ffmpeg.input.return_value.output.return_value.run.return_value = None

    sample_video_path = "./backend/download/downloaded_videos/sample_video.mp4"
    video_clipping_service = VideoClippingService(sample_video_path)
    highlights = [
        {START: "00:00:04.880", END: "00:00:07.950"},
        {START: "00:00:07.960", END: "00:00:12.749"},
        {START: "00:00:12.759", END: "00:00:16.230"}
    ]

    expected_output_paths = [
        f"{sample_video_path.rsplit('.', 1)[0]}_clipped_00:00:04.880_00:00:07.950.mp4",
        f"{sample_video_path.rsplit('.', 1)[0]}_clipped_00:00:07.960_00:00:12.749.mp4",
        f"{sample_video_path.rsplit('.', 1)[0]}_clipped_00:00:12.759_00:00:16.230.mp4"
    ]

    clipped_video_path = video_clipping_service.clip(highlights)

    assert len(clipped_video_path) == 3
    mock_ffmpeg.input.assert_any_call(
        sample_video_path, ss="00:00:04.880", to="00:00:07.950")
    mock_ffmpeg.input.assert_any_call(
        sample_video_path, ss="00:00:07.960", to="00:00:12.749")
    mock_ffmpeg.input.assert_any_call(
        sample_video_path, ss="00:00:12.759", to="00:00:16.230")
    assert clipped_video_path == expected_output_paths
