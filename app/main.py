from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .formatter import fmt
from .yt import parse_video_id, fetch_transcript_text, TranscriptError


app = FastAPI()


BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process", response_class=PlainTextResponse)
async def process(url: str = Form(...), lang: str = Form("auto")):
    vid = parse_video_id(url)
    if not vid:
        return PlainTextResponse("URL から動画IDを取得できませんでした。", status_code=400)


    try:
        raw = fetch_transcript_text(vid, lang_mode=lang)
    except TranscriptError as e:
        return PlainTextResponse(str(e), status_code=400)


    text = fmt(raw)


# ダウンロードさせるため Content-Disposition を付与
    headers = {
    "Content-Disposition": f"attachment; filename={vid}_trimed.txt"
    }
    return PlainTextResponse(text, headers=headers)