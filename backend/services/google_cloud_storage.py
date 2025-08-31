from backend.core.constants import SIGNED_CREDENTIAL_VERSION, URL_EXPIRATION_SECONDS
from backend.core.settings import GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_BUCKET_NAME

from google.cloud import storage
from google.oauth2 import service_account

import os


class GoogleCloudStorage:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            GOOGLE_APPLICATION_CREDENTIALS)
        client = storage.Client(credentials=credentials,
                                project=credentials.project_id)
        self.bucket = client.bucket(GOOGLE_BUCKET_NAME)

    def upload(self, video_paths: list[str]) -> list[str]:
        """Uploads a list of videos to GSC

        Args:
            video_paths (list[str]): A list of video paths

        Returns:
            list[str]: A list of signed urls
        """
        signed_urls = []

        for video_path in video_paths:
            destination_filename = os.path.basename(video_path)

            url = self.upload_one_file(video_path, destination_filename)

            signed_urls.append(url)

        return signed_urls

    def upload_one_file(self, video_path: str, destination_blob: str) -> str:
        """
        Uploads a local file to GCS bucket.

        :param source_file: Path to the local file
        :param destination_blob: The "path" (object name) inside the bucket
        """
        blob = self.bucket.blob(destination_blob)

        # Upload file
        blob.upload_from_filename(video_path)
        print(
            f"File {video_path} uploaded to gs://{GOOGLE_BUCKET_NAME}/{destination_blob}")

        url = blob.generate_signed_url(
            version=SIGNED_CREDENTIAL_VERSION, expiration=URL_EXPIRATION_SECONDS)  # 1 hour

        return url

    def generate_signed_url(self, blob_name: str, expiration_seconds: int = URL_EXPIRATION_SECONDS) -> str:
        """
        Generate a signed URL for a file in GCS.

        :param blob_name: Path to the file in the bucket
        :param expiration_minutes: How long the URL is valid
        :return: Signed URL string
        """
        blob = self.bucket.blob(blob_name)

        if not blob.exists():
            print("Blob does not exist.")
            return ""

        url = blob.generate_signed_url(
            version=SIGNED_CREDENTIAL_VERSION,
            expiration=expiration_seconds,
            method="GET"
        )

        return url


# Example usage
if __name__ == "__main__":
    video_paths = [r"backend/download/downloaded_videos/【Minecraft】視聴者１００人サーバーを観光してみる！！！！！　#結城さくな生放送_clipped_00:28:59.559_00:30:03.799.mp4",
                   r"backend/download/downloaded_videos/【Minecraft】視聴者１００人サーバーを観光してみる！！！！！　#結城さくな生放送_clipped_00:32:07.880_00:33:12.200.mp4",
                   r"backend/download/downloaded_videos/【Minecraft】視聴者１００人サーバーを観光してみる！！！！！　#結城さくな生放送_clipped_00:40:24.040_00:41:27.880.mp4"]
    google_cloud_storage = GoogleCloudStorage()
    signed_urls = google_cloud_storage.upload(video_paths)

    for url in signed_urls:
        print(url)
