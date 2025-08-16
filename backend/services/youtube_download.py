from yt_dlp import YoutubeDL
from backend.core.constants import DOWNLOADED_VIDEO_PATH, DOWNLOADED_AUDIO_PATH

class VideoDownloadService:
    def download(self, video_url: str) -> str:
        """
        Downloads a video from the given URL and returns the file path.
        
        :param video_url: The URL of the video to download.
        :return: The file path where the video is saved.
        """
        output_path = f"{DOWNLOADED_VIDEO_PATH}/%(title)s.%(ext)s"
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best/mp4',
            'outtmpl': output_path,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        return output_path

class AudioDownloadService:
    def download(self, video_url: str) -> str:
        """
        Downloads the audio from the given video URL and returns the file path.
        
        :param video_url: The URL of the video to extract audio from.
        :return: The file path where the audio is saved.
        """
        output_path = f"{DOWNLOADED_AUDIO_PATH}/%(title)s.%(ext)s"
        ydl_opts = {
            'format': 'bestaudio/mp3',
            'outtmpl': output_path,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        return output_path


# Example usage
if __name__ == "__main__":
    video_service = VideoDownloadService()
    audio_service = AudioDownloadService()
    
    video_url = "https://www.youtube.com/watch?v=-MRIkiCRVW8"
    
    video_path = video_service.download(video_url)
    print(f"Video downloaded to: {video_path}")
    
    audio_path = audio_service.download(video_url)
    print(f"Audio downloaded to: {audio_path}") 