from pydantic import BaseModel

class LatexTemplateInfo(BaseModel):
    template_name: str
    template_path: str
