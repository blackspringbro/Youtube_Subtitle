import re


def fmt(text: str) -> str:
    text = re.sub(r"\b\d{1,2}:\d{2}(?::\d{2})?\b", "", text) # 時刻表記削除 0:05 / 1:02:03
    text = re.sub(r"[ \t]*\n+", " ", text) # 改行をスペースに
    text = re.sub(r" {2,}", " ", text) # 連続スペースを1つに
    text = re.sub(r"(?<!\d)\.(\s+|$)", ".\n\n", text) # ピリオドごとに空行
    return text.strip()