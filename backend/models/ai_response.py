from pydantic import BaseModel, Field

from backend.core.constants import HIGHLIGHT_SCORE, REASON


class AIResponse(BaseModel):
    highlight_score: float = Field(
        ..., description="Score indicating the strength of the highlight (0-10)", alias=HIGHLIGHT_SCORE)
    reason: str = Field(...,
                        description="Short explanation of why this is a highlight", alias=REASON)
