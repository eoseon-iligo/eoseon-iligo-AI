# GenerateCommand / GenerateResult
from typing import Literal

from pydantic import BaseModel

from app.domain.models import DocAST


class GenerateCommand(BaseModel):
    format: Literal["docx", "hwpx"]
    ast: DocAST


class GenerateResult(BaseModel):
    filename: str
    content_type: str
    data: bytes
