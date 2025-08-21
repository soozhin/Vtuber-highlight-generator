from datetime import datetime, timedelta

import re

from backend.core.constants import END, START, TEXT, TRANSCRIPT_CHUNK_SIZE


class TranscriptParser:
    def parse(self, vtt_text: str):
        """
        Parses the WebVTT text and returns a list of transcript entries.
        Each entry is a dictionary with 'start', 'end', and 'text' keys.
        """
        transcripts = self.parse_webvtt(vtt_text)
        return self.aggregate_transcripts(transcripts)

    def parse_webvtt(self, vtt_text: str):
        transcripts = []
        pattern = re.compile(
            r"(\d+:\d+:\d+\.\d+)\s+-->\s+(\d+:\d+:\d+\.\d+)[^\n]*\n([^\n]*?)\n(?=(?!\s)|\Z)")

        for match in pattern.finditer(vtt_text):
            start, end, text = match.groups()

            # Clean text
            clean_text = text.strip()

            if clean_text:
                transcripts.append({
                    START: start,
                    END: end,
                    TEXT: clean_text
                })

        return transcripts

    def aggregate_transcripts(self, transcripts):
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
    vtt_path = "./backend/download/downloaded_transcripts/【郡道美玲⧸因幡はねる】サイコパスVtuber最強決定戦【夏色まつり⧸神楽めあ⧸犬山たまき】.ja.vtt"
    with open(vtt_path, 'r', encoding='utf-8') as file:
        vtt_content = file.read()

    parser = TranscriptParser()
    parsed_entries = parser.parse(vtt_content)

    for entry in parsed_entries:
        print(
            f"Start: {entry[START]}, End: {entry[END]}, Text: {entry[TEXT]}")
