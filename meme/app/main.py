from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.utils import generate_meme
import io

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    top_text: str = Form(""),
    bottom_text: str = Form("")
):
    contents = await image.read()
    output_buffer = generate_meme(contents, top_text, bottom_text)
    
    # Determine media type based on original filename or default to jpeg
    media_type = "image/jpeg"
    if image.filename:
        filename = image.filename.lower()
        if filename.endswith(".png"):
            media_type = "image/png"
        elif filename.endswith(".gif"):
            media_type = "image/gif"
    
    return StreamingResponse(output_buffer, media_type=media_type)
