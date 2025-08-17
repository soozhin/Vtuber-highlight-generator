import re


class TranscriptParser:
    def parse_webvtt(self, vtt_text: str):
        entries = []
        pattern = re.compile(
            r"(\d+:\d+:\d+\.\d+)\s+-->\s+(\d+:\d+:\d+\.\d+)[^\n]*\n([^\n]*?)\n(?=(?!\s)|\Z)")

        for match in pattern.finditer(vtt_text):
            start, end, text = match.groups()

            # Clean text
            clean_text = text.strip()

            if clean_text:
                entries.append({
                    "start": start,
                    "end": end,
                    "text": clean_text
                })

        return entries


# Example usage
if __name__ == "__main__":
    vtt_path = "./backend/download/downloaded_transcripts/AZKi： ＂So Many Masochists! What'll Happen To This World？!＂ (Hololive) [Eng Subs].ja.vtt"
    with open(vtt_path, 'r', encoding='utf-8') as file:
        vtt_content = file.read()

    parser = TranscriptParser()
    parsed_entries = parser.parse_webvtt(vtt_content)

    for entry in parsed_entries:
        print(
            f"Start: {entry['start']}, End: {entry['end']}, Text: {entry['text']}")
