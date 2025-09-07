from backend.core.constants import YOUTUBE_REGEX


class UrlValidator:
    def __init__(self):
        pass

    @staticmethod
    def is_validate_url(url: str):
        is_validate_url = bool(YOUTUBE_REGEX.match(url))
        return is_validate_url


# Example usage
if __name__ == "__main__":
    url1 = "random_str1"
    url2 = "https://www.youtube.com/watch?v=UcE0Go6I0XI"

    print(f"Url1 validity: {UrlValidator.is_validate_url(url1)}")   # Url1 validity: False
    print(f"Url2 validity: {UrlValidator.is_validate_url(url2)}")   # Url2 validity: True
    