from backend.services.youtube_download import TranscriptDownloadService, VideoDownloadService
from backend.services.transcript_parser import TranscriptParser
from backend.services.highlight_detection import HighlightDetectionService
from backend.services.video_clipping import VideoClippingService

from typing import List
from concurrent.futures import ThreadPoolExecutor


class GenerateHighlightCoordinator:
    """This class coordinates the generation of highlights in the backend.
    It manages the interaction between different services
    such as video, audio, and transcript download services.
    """

    def run(self, video_url: str) -> List:
        """
        This method coordinates all the services in the backend.
        """

        # Download video and transcript
        video_service = VideoDownloadService()
        transcript_service = TranscriptDownloadService()

        with ThreadPoolExecutor(max_workers=1) as executor:
            # Download video on a different thread
            video_future = executor.submit(video_service.download, video_url)

            transcript_path = transcript_service.download(video_url)
            print(f"Transcript downloaded to: {transcript_path}")

            # Parse the transcript
            parser = TranscriptParser()
            parsed_entries = parser.parse(transcript_path)
            print(f"Parsed Transcript Entries count: {len(parsed_entries)}")

            # Detect highlights from the parsed transcript
            highlight_service = HighlightDetectionService()
            highlights = highlight_service.execute(parsed_entries)
            print(f"Detected Highlights count: {len(highlights)}")

            # Clip the video based on detected highlights
            video_path = video_future.result()
            video_clipping_service = VideoClippingService(video_path)
            clipped_videos = video_clipping_service.clip(highlights)
            print(f"Clipped Videos: {clipped_videos}")

        return clipped_videos


# Example usage
if __name__ == "__main__":
    highlight_generator = GenerateHighlightCoordinator()
    video_url = "https://www.youtube.com/watch?v=UcE0Go6I0XI"
    clipped_videos = highlight_generator.run(video_url)

    print("Clipped Videos:")
    for video in clipped_videos:
        print(video)
