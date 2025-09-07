from pydantic import BaseModel, Field
from typing import List


class GenerateHighlightResponse(BaseModel):
    download_links: List[str | None] = Field(...,
                                             description="A list of downloadable links")
