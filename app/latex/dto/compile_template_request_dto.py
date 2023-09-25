
from pydantic import BaseModel
from ..models.latex_variable_info import LatexVariableInfo

class CompileTemplateRequestDto(BaseModel):
    template_name: str
    template_variables: list[LatexVariableInfo]