from typing import Optional
from pydantic import BaseModel


class CompileVariableInfo(BaseModel):
    name: str
    value: Optional[str]
