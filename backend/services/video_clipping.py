from typing import List
import ffmpeg

from backend.core.constants import END, START


class VideoClippingService:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.video_path_wo_ext = video_path.rsplit('.', 1)[0]
        

    def clip(self, highlights: List) -> List:
        """
        Clips all highlights from start_time to end_time and saves it.

        :param highlights: List of dictionaries with 'start_time' and 'end_time'
        :return: Path to the clipped video
        """
        output_videos = []
        for highlight in highlights:
            start_time = highlight.get(START, "00:00:00.000")
            end_time = highlight.get(END, "00:00:10.000")
            clipped_video_path = f"{self.video_path_wo_ext}_clipped_{start_time}_{end_time}.mp4"

            (
                ffmpeg
                .input(self.video_path, ss=start_time, to=end_time)
                .output(clipped_video_path, c='copy')
                .run()
            )

            output_videos.append(clipped_video_path)

        return output_videos


# Example usage
if __name__ == "__main__":
    video_clipping_service = VideoClippingService(
        "./backend/download/downloaded_videos/＂Soda Pop＂ Official Lyric Video ｜ KPop Demon Hunters ｜ Sony Animation.webm")

    highlights = [
        {START: "00:00:04.880", END: "00:00:07.950"},
        {START: "00:00:07.960", END: "00:00:12.749"},
        {START: "00:00:12.759", END: "00:00:16.230"}
    ]

    clipped_video_path = video_clipping_service.clip(highlights)

    print(f"Clipped Video Path: {clipped_video_path}")
