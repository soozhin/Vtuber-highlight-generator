from fastapi import APIRouter
from fastapi import HTTPException

from backend.models.generate_highlight_request import GenereateHighlightRequest
from backend.models.generate_highlight_response import GenerateHighlightResponse
from backend.services.generate_highlight_coordinator import GenerateHighlightCoordinator
from backend.services.url_validator import UrlValidator

router = APIRouter()


@router.post("/generate-highlight",
             response_model=GenerateHighlightResponse,
             description="Takes in a youtube url, clips highlight and return downloadable links to the clip.")
async def generate_highlight(highlight_request: GenereateHighlightRequest):
    if not UrlValidator.is_validate_url(highlight_request.url):
        raise HTTPException(400, "Invalid url")

    try:
        highlight_coordinator = GenerateHighlightCoordinator()
        highlight_response: GenerateHighlightResponse = highlight_coordinator.run(
            highlight_request.url)
        return highlight_response
    except Exception as e:
        raise HTTPException(500, str(e.with_traceback))
