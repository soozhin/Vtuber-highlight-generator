from pydantic import BaseModel, Field


class GenereateHighlightRequest(BaseModel):
    url: str = Field(..., description="A YouTube URL of a Vtuber livestream")
