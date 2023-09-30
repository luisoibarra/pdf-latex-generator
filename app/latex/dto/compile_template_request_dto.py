
from pydantic import BaseModel
from ..models.compile_variable_info import CompileVariableInfo

class CompileTemplateRequestDto(BaseModel):
    template_name: str
    template_variables: list[CompileVariableInfo]