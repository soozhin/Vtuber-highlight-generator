import random
from backend.core.constants import END, HIGHLIGHT_DETECTION_PROMPT, HIGHLIGHT_SCORE, MAX_SCORE, MIN_SCORE, REASON, START, TEXT, THRESHOLD_SCORE
from backend.core.settings import GOOGLE_AI_API_KEY
from backend.models.ai_response import AIResponse

from google import genai

import json
import re


class HighlightDetectionService:
    def __init__(self):
        self.client = genai.Client(api_key=GOOGLE_AI_API_KEY)

    def execute(self, transcripts: list) -> list:
        """
        Execute highlight detection on the provided transcripts.
        """
        if not transcripts:
            return []

        # Score each transcript entry for highlights
        scored_transcripts = self.score_transcripts(transcripts)

        # Filter out entries with highlight score of 0
        highlights = self.detect_highlights(scored_transcripts)

        # Aggregate highlights based on their start and end times
        aggregated_highlights = self.aggregate_highlights(highlights)

        return aggregated_highlights

    def aggregate_highlights(self, highlights: list) -> list:
        """
        Aggregate highlights based on their start and end times.
        """
        if not highlights:
            return []

        aggregated_highlights = []
        current_highlight = highlights[0]

        for highlight in highlights[1:]:
            # Ignore milliseconds for comparison
            if highlight[START][:-4] == current_highlight[END][:-4]:
                # Overlapping or contiguous highlights, extend the current one
                current_highlight[END] = highlight[END]
                current_highlight[TEXT] += " " + highlight[TEXT]
                current_highlight[HIGHLIGHT_SCORE] = max(
                    current_highlight.get(HIGHLIGHT_SCORE, 0),
                    highlight.get(HIGHLIGHT_SCORE, 0)
                )
                current_highlight[REASON] += " " + highlight.get(REASON, "")
            else:
                # No overlap, save the current highlight and start a new one
                aggregated_highlights.append(current_highlight)
                current_highlight = highlight

        # Add the last highlight
        aggregated_highlights.append(current_highlight)

        return aggregated_highlights

    def detect_highlights(self, scored_transcripts: list) -> list:
        """
        Detect highlights using the scored transcripts with threshold value 
        defined in constants.
        """
        if not scored_transcripts:
            return []

        # Filter out entries with highlight score of 0
        highlights = [t for t in scored_transcripts if t.get(
            HIGHLIGHT_SCORE, 0) > THRESHOLD_SCORE]

        return highlights

    def score_transcripts(self, transcripts: list) -> list:
        """
        Detect highlights in the video.
        """
        transcsript_score = []

        for transcript in transcripts:
            # AI promps for highlight detection

            prompt = HIGHLIGHT_DETECTION_PROMPT % transcript[TEXT]

            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
            )
            resp_text = response.text

            # For testing purposes, we will use a dummy response
            # In production, uncomment the above lines and comment the below lines
            # dummy_response = {
            #     HIGHLIGHT_SCORE: random.uniform(MIN_SCORE, MAX_SCORE),
            #     REASON: "Dummy data"
            # }
            # resp_text = "```json\n" + \
            #     str(dummy_response).replace("'", '"') + "\n```"

            try:
                cleaned = re.sub(r"^```(?:json)?\s*", "", resp_text.strip())
                cleaned = re.sub(r"\s*```$", "", cleaned)
                resp_json = json.loads(cleaned)
                ai_resp = AIResponse(
                    highlight_score=float(resp_json.get(HIGHLIGHT_SCORE, 0)),
                    reason=resp_json.get(REASON, "No reason provided")
                )
                transcript[HIGHLIGHT_SCORE] = ai_resp.highlight_score
                transcript[REASON] = ai_resp.reason
            except Exception as e:
                # fallback in case parsing fails
                ai_resp = AIResponse(
                    highlight_score=0,
                    reason="Failed to parse AI response"
                )
                transcript[HIGHLIGHT_SCORE] = 0
                transcript[REASON] = "Failed to parse AI response"

            transcsript_score.append(transcript)

        return transcsript_score


# Example usage
if __name__ == "__main__":
    highlight_detection_service = HighlightDetectionService()
    transcripts = [{START: '00:01:33.720', END: '00:02:37.460',
                    TEXT: '[音楽] ben ん [音楽] ana 持っています [音楽] [音楽] ん 多分ん ハーイご主人様ワンタワー男の壁一重バーの犬山た秋です ということでねえっとサムネイルと bgm が全く合ってないんですけどもこのまま 異国なと思いますということで皆さんついにこの日がやってまいりましたそれでは栄光 をかけていきましょう サイコパス v 中ば最強受けて1000回へ [拍手] はいということで始まりましたサイコば水中バー最強決定戦へこちらの企画はですね'},
                   {START: '00:02:37.470', END: '00:03:41.160', TEXT: 'えっとなんでこの企画やることになったかと言いますとあの以前ね夏への祭りさんと あのサンリオピューロランドで遊びに行ったことがあったんですけども その時にまあなんかね色々あの順番待ちで並んでいる時に暇だったんで あの祭にサイコパス診断を少しやってみたんですよ まあ市松伏ねそんじゃないんですねあの第一問からぱっちこり正解はのやつはね当てて きまして 本当にこれって当ててくる奴いるんだって思って サイコパスの新蘭が出るぞ正解をねまぁすれば正解ってばいいんですけどあの祭りです よ だしてきまして僕もねあの昔サイコパス診断自分でちょっとやったことあるんですけど あの一般人の回答しかちょっと出せなくてですね あのそこでまぁツイッターでサイコパスっぽい v 中ば誰ですかあって質問した ところ 特に多かった8人を本日およびさせていただきました ということで呼び込みしていきましょう まず1人目我らが組長いなーバー派手でさーんどうぞ'},
                   {START: '00:03:41.170', END: '00:04:45.590', TEXT: 'あまあまあシュルしくお願いしません続所 いえなかこんな中そうそうたる サイコパスのメンバーになぁかちょっと私なぁかが混じってしまって大丈夫かなぁと 思ってヘナか本当に申し訳ないで市民ならー過去 他の方ほんとねせぱすといえばー みてーな方ばっかりなのにそんな彼に私なんかが無しってしまって皆ちょっと場違い カラーなんてちょっと思って申し訳ないんだと思ってませんあり今日もしかしね大きい ですか違いますねやっぱり安定さあねおかげとリフェコアのかわいいせんですよねー ですねええええ あれいう宇宙はますし普段増力さん逆ですかな感じで好きで エレアコ山通りの感じです良いもう様子を塗るキャンを申し訳ない バーン罰がいいか王者自分ではリプライ多かった気がするんですけどねそうか彦 ましたあなたも間違えだなぁ 学部者売名とか恐れございます 封印ないして中韓に行ったんだけど誰だかやらだソロ育てなのか'},
                   {START: '00:04:45.600', END: '00:05:49.720', TEXT: 'いや親父あの花さあのチケット完売おめでとうございますありがとうございまして皆れ 来てくださいのバーナー完璧車来てございませんけどイベントも うん マネージャー本日頑張ってくださいよろしくお願いしますこれ一応確認しておくとイア の中受けねないとかサイコパスのなぁ回答何か狙ったできるとかじゃなくてはい国家 いいなぁか思ったとおりにすごいにくいいう形んよね 妻もいいですが近いと俺じゃない大丈夫っすそうだよねあのじゃあ 本当に取れ高ないと思うんですけどよろしくお願いシャンあるがチクリとなのかなる ほどね うまっっわかりましたはいということでじゃあ続いて2人目を呼びしていきましょう 続いてはこの方 かぐら姐さーん'},
                   ]
    highlights = highlight_detection_service.execute(transcripts)

    for highlight in highlights:
        print(f"Start: {highlight[START]}, End: {highlight[END]}, "
              f"Text: {highlight[TEXT]}, "
              f"Highlight Score: {highlight.get(HIGHLIGHT_SCORE, 'N/A')}, "
              f"Reason: {highlight.get(REASON, 'N/A')}")
    print("\nHighlight detection completed.\n")
