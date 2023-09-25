from typing import Optional
from pydantic import BaseModel


class LatexVariableInfo(BaseModel):
    name: str
    value: Optional[str]
