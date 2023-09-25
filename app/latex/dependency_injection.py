from pathlib import Path
from typing import Optional
from .main import get_latex_template
from .models.latex_template_info import LatexTemplateInfo
from .models.latex_variable_info import LatexVariableInfo
from .config import LatexConfig

class LatexTemplateInfoRepository:
    def __init__(self) -> None:
        self.path = Path(LatexConfig.TEMPLATE_DIR)
    
    def get_all_templates(self) -> list[LatexTemplateInfo]:
        return [LatexTemplateInfo(template_name=x.name, template_path=str(x)) 
                for x in self.path.iterdir() if x.is_dir()]

    def get_template_info_by_name(self, template_name: str) -> Optional[LatexTemplateInfo]:
        templates = [x for x in self.get_all_templates() if x.template_name == template_name]
        if templates:
            return templates[0]
        return None

class LatexEngineService:
    async def get_compiled_pdf_bytes(self, template: LatexTemplateInfo, template_variables: list[LatexVariableInfo]) -> bytes:
        return await get_latex_template(template, template_variables)
