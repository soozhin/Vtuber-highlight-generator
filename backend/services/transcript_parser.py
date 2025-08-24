from datetime import datetime, timedelta
from typing import List

import json

from backend.core.constants import DURATION, END, START, TEXT, TRANSCRIPT_CHUNK_SIZE


class TranscriptParser:
    def parse(self, transctipts_path: str):
        """
        Parses the WebVTT text and returns a list of transcript entries.
        Each entry is a dictionary with 'start', 'end', and 'text' keys.
        """
        transcripts = self._extract_json(transctipts_path)
        transcripts = self._parse_transcripts(transcripts)
        return self._aggregate_transcripts(transcripts)

    def _extract_json(self, transctipts_path: str) -> List:
        with open(transctipts_path, 'r') as file:
            transctipts = json.load(file)
        return transctipts

    def _parse_transcripts(self, transcripts_raw: str):
        transcripts = []

        for i, chunk in enumerate(transcripts_raw):
            text = chunk[TEXT]
            start_sec = chunk[START]

            if i < len(transcripts_raw) - 1:
                end_sec = transcripts_raw[i+1][START]
            else:
                end_sec = chunk[DURATION] + start_sec

            start = self._format_seconds(start_sec)
            end = self._format_seconds(end_sec)

            # Clean text
            clean_text = text.strip()

            if clean_text:
                transcripts.append({
                    START: start,
                    END: end,
                    TEXT: clean_text
                })

        return transcripts

    def _format_seconds(self, seconds: float) -> str:
        td = timedelta(seconds=seconds)
        total_seconds = td.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        secs = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{secs:06.3f}"  # HH:MM:SS.mmm

    def _aggregate_transcripts(self, transcripts):
        aggregated = []
        aggregated_text = ""
        previous_start_time = None
        for transcript in transcripts:
            start = transcript[START]
            end = transcript[END]
            text = transcript[TEXT]
            current_start_time = datetime.strptime(start, "%H:%M:%S.%f")
            current_end_time = datetime.strptime(end, "%H:%M:%S.%f")
            aggregated_text = aggregated_text + " " + text

            if previous_start_time is None:
                previous_start_time = current_start_time

            if current_end_time - previous_start_time > timedelta(seconds=TRANSCRIPT_CHUNK_SIZE) or transcript == transcripts[-1]:
                aggregated.append({
                    START: datetime.strftime(previous_start_time, "%H:%M:%S.%f")[:-3],
                    END: end,
                    TEXT: str.strip(aggregated_text)
                })
                aggregated_text = ""
                previous_start_time = None

        return aggregated


# Example usage
if __name__ == "__main__":
    vtt_path = "./backend/download/downloaded_transcripts/【恋バナ】超絶ノンデリ彼ピと！念願の恋愛相談読んでみる・・・よッ！【にじさんじ_星川サラ_犬山たまき】#星川恋愛研究所.json"

    parser = TranscriptParser()
    parsed_entries = parser.parse(vtt_path)

    for entry in parsed_entries:
        print(
            f"Start: {entry[START]}, End: {entry[END]}, Text: {entry[TEXT]}")
