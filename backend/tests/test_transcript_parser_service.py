from backend.services.transcript_parser import TranscriptParser
from textwrap import dedent


def test_parse_webvtt():
    # Sample VTT content
    vtt_content = """
    WEBVTT
    Kind: captions
    Language: ja

    00:00:00.160 --> 00:00:04.870 align:start position:0%
    
    いやあ<00:00:00.480><c>、</c><00:00:00.680><c>まあ</c><00:00:01.520><c>昨日</c><00:00:02.240><c>は</c><00:00:02.440><c>ね</c><00:00:02.679><c>、</c><00:00:03.639><c>大変</c><00:00:03.959><c>な</c><00:00:04.080><c>1</c><00:00:04.319><c>日</c><00:00:04.520><c>だっ</c><00:00:04.759><c>た</c>

    00:00:04.870 --> 00:00:04.880 align:start position:0%
    いやあ、まあ昨日はね、大変な1日だった
    

    00:00:04.880 --> 00:00:07.950 align:start position:0%
    いやあ、まあ昨日はね、大変な1日だった
    。<00:00:05.279><c>もう</c><00:00:05.560><c>それ</c><00:00:05.799><c>以外</c><00:00:06.120><c>の</c><00:00:06.279><c>こと</c><00:00:06.480><c>が</c><00:00:06.680><c>何</c><00:00:06.879><c>も</c><00:00:07.120><c>考え</c><00:00:07.439><c>られ</c><00:00:07.799><c>な</c>

    00:00:07.950 --> 00:00:07.960 align:start position:0%
    。もうそれ以外のことが何も考えられな
    

    00:00:07.960 --> 00:00:12.749 align:start position:0%
    。もうそれ以外のことが何も考えられな
    すぎ<00:00:08.200><c>て</c><00:00:09.080><c>1</c><00:00:09.320><c>日</c><00:00:10.559><c>なんか</c><00:00:11.480><c>ぼーっと</c><00:00:11.920><c>し</c><00:00:12.040><c>て</c><00:00:12.120><c>過ごし</c><00:00:12.480><c>て</c><00:00:12.599><c>た</c>

    00:00:12.749 --> 00:00:12.759 align:start position:0%
    すぎて1日なんかぼーっとして過ごしてた
    

    00:00:12.759 --> 00:00:16.230 align:start position:0%
    すぎて1日なんかぼーっとして過ごしてた
    """

    # Expected parsed entries
    expected_entries = [
        {"start": "00:00:04.880", "end": "00:00:07.950",
            "text": "いやあ、まあ昨日はね、大変な1日だった"},
        {"start": "00:00:07.960", "end": "00:00:12.749",
            "text": "。もうそれ以外のことが何も考えられな"},
        {"start": "00:00:12.759", "end": "00:00:16.230",
            "text": "すぎて1日なんかぼーっとして過ごしてた"}
    ]

    # Create an instance of the TranscriptParserService
    parser_service = TranscriptParser()

    # Parse the VTT content
    parsed_entries = parser_service.parse_webvtt(dedent(vtt_content))

    # Assert that the parsed entries match the expected entries
    assert parsed_entries == expected_entries


def test_aggregate_transcripts():
    # Sample parsed entries
    parsed_entries = [
        {"start": "00:00:04.880", "end": "00:00:59.950",
            "text": "いやあ、まあ昨日はね、大変な1日だった"},
        {"start": "00:00:59.960", "end": "00:01:12.749",
            "text": "。もうそれ以外のことが何も考えられな"},
        {"start": "00:01:12.759", "end": "00:02:16.230",
            "text": "すぎて1日なんかぼーっとして過ごしてた"},
        {"start": "00:02:16.230", "end": "00:02:19.230", "text": "AAA"}
    ]

    # Expected aggregated entries
    expected_aggregated = [
        {"start": "00:00:04.880", "end": "00:01:12.749",
            "text": "いやあ、まあ昨日はね、大変な1日だった 。もうそれ以外のことが何も考えられな"},
        {"start": "00:01:12.759", "end": "00:02:16.230",
            "text": "すぎて1日なんかぼーっとして過ごしてた"},
        {"start": "00:02:16.230", "end": "00:02:19.230", "text": "AAA"}
    ]

    # Create an instance of the TranscriptParserService
    parser_service = TranscriptParser()

    # Aggregate the transcripts
    aggregated_entries = parser_service.aggregate_transcripts(parsed_entries)

    # Assert that the aggregated entries match the expected entries
    assert aggregated_entries == expected_aggregated
