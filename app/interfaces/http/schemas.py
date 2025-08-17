# FastAPI 입출력 스키마(GenerateReqeust/Response)

from typing import Literal, Optional
from pydantic import BaseModel
from app.domain.models import DocAST

from typing import Literal
from pydantic import BaseModel
from app.domain.models import DocAST

class GenerateRequest(BaseModel):
    format: Literal["docx", "hwpx"]
    ast: DocAST

class GenerateResponse(BaseModel):
    filename: str
    content_type: str
    server_path: Optional[str] = None