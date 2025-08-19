from backend.core.constants import END, HIGHLIGHT_SCORE, REASON, START, TEXT
from backend.services.highlight_detection import HighlightDetectionService
from unittest.mock import patch, MagicMock


@patch("backend.services.highlight_detection.genai.Client")
def test_score_transcripts(client_mock):
    service = HighlightDetectionService()

    ai_response_mock = MagicMock()
    ai_response_mock.text = '```json\n{"highlight_score": 0.8, "reason": "mock reason"}\n```'

    client_mock_instance = client_mock.return_value
    client_mock_instance.models.generate_content.return_value = ai_response_mock

    transcripts = [
        {
            START: "00:00:01.000",
            END: "00:00:05.000",
            TEXT: "This is a test highlight."
        },
        {
            START: "00:00:06.000",
            END: "00:00:10.000",
            TEXT: "This is another highlight."
        }
    ]

    scored_transcripts = service.score_transcripts(transcripts)

    assert len(scored_transcripts) == 2
    assert scored_transcripts[0][HIGHLIGHT_SCORE] == 0.8
    assert scored_transcripts[0][REASON] == "mock reason"
    assert scored_transcripts[0][START] == "00:00:01.000"
    assert scored_transcripts[0][END] == "00:00:05.000"
    assert scored_transcripts[0][TEXT] == "This is a test highlight."
    assert scored_transcripts[1][START] == "00:00:06.000"
    assert scored_transcripts[1][END] == "00:00:10.000"
    assert scored_transcripts[1][TEXT] == "This is another highlight."
    assert scored_transcripts[1][HIGHLIGHT_SCORE] == 0.8
    assert scored_transcripts[1][REASON] == "mock reason"


def test_detect_highlights():
    service = HighlightDetectionService()

    transcripts = [
        {
            START: "00:00:01.000",
            END: "00:00:05.000",
            TEXT: "This is a test highlight.",
            HIGHLIGHT_SCORE: 8,
            REASON: "Interesting moment"
        },
        {
            START: "00:00:06.000",
            END: "00:00:10.000",
            TEXT: "This is another highlight.",
            HIGHLIGHT_SCORE: 0,
            REASON: "Not interesting"
        },
        {
            START: "00:00:11.000",
            END: "00:00:15.000",
            TEXT: "This is a third highlight.",
            HIGHLIGHT_SCORE: 9,
            REASON: "Very interesting"
        }
    ]

    highlights = service.detect_highlights(transcripts)

    assert len(highlights) == 2
    assert highlights[0][START] == "00:00:01.000"
    assert highlights[0][END] == "00:00:05.000"
    assert highlights[0][TEXT] == "This is a test highlight."
    assert highlights[0][HIGHLIGHT_SCORE] == 8
    assert highlights[0][REASON] == "Interesting moment"
    assert highlights[1][START] == "00:00:11.000"
    assert highlights[1][END] == "00:00:15.000"
    assert highlights[1][TEXT] == "This is a third highlight."
    assert highlights[1][HIGHLIGHT_SCORE] == 9
    assert highlights[1][REASON] == "Very interesting"


def test_aggregate_highlights():
    service = HighlightDetectionService()

    highlights = [
        {
            START: "00:00:01.000",
            END: "00:00:05.000",
            TEXT: "This is a test highlight.",
            HIGHLIGHT_SCORE: 8,
            REASON: "Interesting moment"
        },
        {
            START: "00:00:05.000",
            END: "00:00:10.000",
            TEXT: "This is another highlight.",
            HIGHLIGHT_SCORE: 9,
            REASON: "Very interesting"
        },
        {
            START: "00:00:11.000",
            END: "00:00:15.000",
            TEXT: "This is a third highlight.",
            HIGHLIGHT_SCORE: 7,
            REASON: "Somewhat interesting"
        }
    ]

    aggregated_highlights = service.aggregate_highlights(highlights)

    assert len(aggregated_highlights) == 2
    assert aggregated_highlights[0][START] == "00:00:01.000"
    assert aggregated_highlights[0][END] == "00:00:10.000"
    assert aggregated_highlights[0][TEXT] == "This is a test highlight. This is another highlight."
    assert aggregated_highlights[0][HIGHLIGHT_SCORE] == 9
    assert aggregated_highlights[0][REASON] == "Interesting moment Very interesting"

    assert aggregated_highlights[1][START] == "00:00:11.000"
    assert aggregated_highlights[1][END] == "00:00:15.000"
    assert aggregated_highlights[1][TEXT] == "This is a third highlight."
    assert aggregated_highlights[1][HIGHLIGHT_SCORE] == 7
    assert aggregated_highlights[1][REASON] == "Somewhat interesting"
