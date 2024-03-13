from pathlib import Path
from typing import Optional
import shutil
import logging

from .config import LatexConfig, WordConfig
from .engine.compile_engine import LatexCompiler, WordCompiler
from .models.compile_variable_info import CompileVariableInfo
from .models.template_info import TemplateInfo
from .engine.template_engine import LatexTemplateEngine, WordTemplateEngine

class LatexTemplateInfoRepository:
    def __init__(self) -> None:
        self.path = Path(LatexConfig.TEMPLATE_DIR)
    
    def get_all_templates(self) -> list[TemplateInfo]:
        return [TemplateInfo(template_name=x.name, template_path=str(x)) 
                for x in self.path.iterdir() if x.is_dir()]

    def get_template_info_by_name(self, template_name: str) -> Optional[TemplateInfo]:
        templates = [x for x in self.get_all_templates() if x.template_name == template_name]
        if templates:
            return templates[0]
        return None

class LatexEngineService:
    async def get_compiled_pdf_bytes(self, template: TemplateInfo, template_variables: list[CompileVariableInfo]) -> bytes:
        return await get_latex_template(template, template_variables)

class WordTemplateInfoRepository:
    def __init__(self) -> None:
        self.path = Path(WordConfig.TEMPLATE_DIR)
    
    def get_all_templates(self) -> list[TemplateInfo]:
        return [TemplateInfo(template_name=x.name, template_path=str(x)) 
                for x in self.path.iterdir() if x.is_dir()]

    def get_template_info_by_name(self, template_name: str) -> Optional[TemplateInfo]:
        templates = [x for x in self.get_all_templates() if x.template_name == template_name]
        if templates:
            return templates[0]
        return None

class WordEngineService:
    async def get_compiled_pdf_bytes(self, template: TemplateInfo, template_variables: list[CompileVariableInfo]) -> bytes:
        return await get_word_template(template, template_variables)


async def get_latex_template(info: TemplateInfo, variables: list[CompileVariableInfo]) -> bytes:
    """
    Returns the template bytes for the latex compiled pdf usign given variables.
    """
    engine = LatexTemplateEngine()
    compiler = LatexCompiler()

    temp_template = None
    try:
        temp_template = engine.add_variable_values_to_template(info, variables)
        pdf_path = await compiler.compile(temp_template)
        pdf_path = Path(pdf_path)
        return pdf_path.read_bytes()
    except Exception as e:
        logging.error(e)
        raise e
    finally:
        if temp_template is None:
            raise Exception(f"Failed to add variables values to template {info.template_name}")
        try:
            shutil.rmtree(temp_template.template_path)
        except Exception as e:
            logging.error(f"Unable to delete temporary template path {temp_template.template_path} because: " + str(e))
            raise

async def get_word_template(info: TemplateInfo, variables: list[CompileVariableInfo]) -> bytes:
    """
    Returns the template bytes for the word compiled pdf usign given variables.
    """
    engine = WordTemplateEngine()
    compiler = WordCompiler()

    temp_template = None
    try:
        temp_template = engine.add_variable_values_to_template(info, variables)
        pdf_path = await compiler.compile(temp_template)
        pdf_path = Path(pdf_path)
        return pdf_path.read_bytes()
    except Exception as e:
        logging.error(e)
        raise e
    finally:
        if temp_template is None:
            raise Exception(f"Failed to add variables values to template {info.template_name}")
        try:
            shutil.rmtree(temp_template.template_path)
        except Exception as e:
            logging.error(f"Unable to delete temporary template path {temp_template.template_path} because: " + str(e))
            raise
