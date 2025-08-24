from backend.core.constants import END, START, TEXT
from backend.services.transcript_parser import TranscriptParser
from textwrap import dedent


def test_parse_transcripts():
    # Sample VTT content
    json_content = [
        {
            "text": "A",
            "start": 0.0,
            "duration": 5
        },
        {
            "text": "B",
            "start": 5.0,
            "duration": 40.0
        },
        {
            "text": "C",
            "start": 90.0,
            "duration": 3
        },
    ]

    # Expected parsed entries
    expected_entries = [
        {START: "00:00:00.000", END: "00:00:05.000",
            TEXT: "A"},
        {START: "00:00:05.000", END: "00:01:30.000",
            TEXT: "B"},
        {START: "00:01:30.000", END: "00:01:33.000",
            TEXT: "C"}
    ]

    # Create an instance of the TranscriptParserService
    parser_service = TranscriptParser()

    # Parse the VTT content
    parsed_entries = parser_service._parse_transcripts(json_content)

    # Assert that the parsed entries match the expected entries
    assert parsed_entries == expected_entries


def test_aggregate_transcripts():
    # Sample parsed entries
    parsed_entries = [
        {START: "00:00:04.880", END: "00:00:59.950",
            TEXT: "いやあ、まあ昨日はね、大変な1日だった"},
        {START: "00:00:59.960", END: "00:01:12.749",
            TEXT: "。もうそれ以外のことが何も考えられな"},
        {START: "00:01:12.759", END: "00:02:16.230",
            TEXT: "すぎて1日なんかぼーっとして過ごしてた"},
        {START: "00:02:16.230", END: "00:02:19.230", TEXT: "AAA"}
    ]

    # Expected aggregated entries
    expected_aggregated = [
        {START: "00:00:04.880", END: "00:01:12.749",
            TEXT: "いやあ、まあ昨日はね、大変な1日だった 。もうそれ以外のことが何も考えられな"},
        {START: "00:01:12.759", END: "00:02:16.230",
            TEXT: "すぎて1日なんかぼーっとして過ごしてた"},
        {START: "00:02:16.230", END: "00:02:19.230", TEXT: "AAA"}
    ]

    # Create an instance of the TranscriptParserService
    parser_service = TranscriptParser()

    # Aggregate the transcripts
    aggregated_entries = parser_service._aggregate_transcripts(parsed_entries)

    # Assert that the aggregated entries match the expected entries
    assert aggregated_entries == expected_aggregated
