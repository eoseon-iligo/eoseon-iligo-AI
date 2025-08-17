# DocAST / Section/Table:문서의 논리 구조
from typing import List, Optional
from pydantic import BaseModel, Field

class Table(BaseModel):
    headers: List[str]
    rows: List[List[str]]

class Section(BaseModel):
    heading: Optional[str] = None
    body: Optional[str] = None
    tables: Optional[List[Table]] = None

class DocAST(BaseModel):
    title: Optional[str] = None
    sections: List[Section] = Field(default_factory=list)
    footer: Optional[str] = None