from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


LANG_PRESETS = {
"auto": [
"ja", "ja-JP", "a.ja", "a.ja-JP",
"en", "en-US", "en-GB", "a.en", "a.en-US", "a.en-GB",
],
"ja": ["ja", "ja-JP", "a.ja", "a.ja-JP"],
"en": ["en", "en-US", "en-GB", "a.en", "a.en-US", "a.en-GB"],
}


def parse_video_id(url: str) -> str:
    u = urlparse(url)
    if u.netloc.endswith("youtu.be"):
        vid = u.path.lstrip("/")
        return vid.split("/")[0]
    if "watch" in u.path:
        return parse_qs(u.query).get("v", [""])[0]
    parts = [p for p in u.path.split("/") if p]
    if parts:
        if len(parts) >= 2 and parts[0] in ("shorts", "embed", "live"):
            return parts[1]
        return parts[-1]
    return ""


class TranscriptError(Exception):
    pass


def fetch_transcript_text(video_id: str, lang_mode: str = "auto") -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=LANG_PRESETS.get(lang_mode, LANG_PRESETS["auto"]))
        lines = [chunk.get("text", "").strip() for chunk in transcript if chunk.get("text", "").strip()]
        return "\n".join(lines)
    except TranscriptsDisabled as e:
        raise TranscriptError("この動画は字幕が無効化されています。") from e
    except NoTranscriptFound as e:
        raise TranscriptError("この動画の字幕が見つかりません（対応言語なし／未提供）。") from e
    except Exception as e:
        raise TranscriptError(f"字幕取得中にエラー: {e}") from e