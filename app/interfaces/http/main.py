from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import io, time, uuid
from pathlib import Path

from app.interfaces.http.schemas import GenerateRequest, GenerateResponse
from app.application.use_cases.generate_document import GenerateDocumentUseCase
from app.application.dto import GenerateCommand
from app.infrastructure.renderers.docx_renderer import DocxRenderer
from app.infrastructure.renderers.hwpx_renderer import HwpxRenderer
from app.infrastructure.config import settings

app = FastAPI(title="BattleShip API (Clean Architecture)")

_RENDERERS = {
    "docx": DocxRenderer(),
    "hwpx": HwpxRenderer(),
}

from cowpy import cow 

@app.get("/")
def greeting():
    return cow.Moose().milk("Hello BattleShip")

@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    renderer = _RENDERERS.get(req.format)
    if not renderer:
        raise HTTPException(status_code=400, detail="Unsupported format")

    usecase = GenerateDocumentUseCase(renderer)
    result = usecase.execute(GenerateCommand(format=req.format, ast=req.ast))

    settings.storage_dir.mkdir(parents=True, exist_ok=True)

    ts = time.strftime("%Y%m%d-%H%M%S")
    ext = ".docx" if req.format == "docx" else ".hwpx"
    fname = f"{ts}-{uuid.uuid4().hex[:8]}{ext}"
    server_path = settings.storage_dir / fname

    with open(server_path, "wb") as f:
        f.write(result.data)

    return GenerateResponse(
        filename=result.filename,               
        content_type=result.content_type,
        server_path=str(server_path.resolve()), 
    )

from pathlib import Path
import time

OUTPUT_DIR = Path.cwd() / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/download")
async def download(req: GenerateRequest):
    renderer = _RENDERERS.get(req.format)
    if not renderer:
        raise HTTPException(status_code=400, detail="Unsupported format")

    usecase = GenerateDocumentUseCase(renderer)
    result = usecase.execute(GenerateCommand(format=req.format, ast=req.ast))

    ts = time.strftime("%Y%m%d-%H%M%S")
    server_path = OUTPUT_DIR / f"{ts}-{result.filename}"
    with open(server_path, "wb") as f:
        f.write(result.data)

    return StreamingResponse(
        io.BytesIO(result.data),
        media_type=result.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={result.filename}",
            "X-Server-Path": str(server_path),  
        },
    )

def run():
    """Entry point for `poetry run docgen-api`"""
    import uvicorn
    uvicorn.run("app.interfaces.http.main:app", host="0.0.0.0", port=8002, reload=True)
