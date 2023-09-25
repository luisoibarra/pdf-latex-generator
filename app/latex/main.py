from pathlib import Path
import shutil
import logging
from typing import Optional
from .engine.template_engine import RegexTemplateEngine
from .engine.compile_engine import LatexCompiler
from .models.latex_template_info import LatexTemplateInfo
from .models.latex_variable_info import LatexVariableInfo

async def test_latex_flow():
    try:
        template = RegexTemplateEngine().add_variable_values_to_template(
            LatexTemplateInfo(
                template_name="LaTeXTemplates_minimal-memo_v1.0",
                template_path=str(Path(__file__, "..", "templates",
                                "LaTeXTemplates_minimal-memo_v1.0").resolve()),
            ),
            title="Template Test",
            first_line="THIS IS THE FIRST LINE OF THE BODY. PLACED BY TEMPLATE ENGINE",
        )
        await LatexCompiler().compile(template)
    finally:
        try:
            shutil.rmtree(template.template_path)
        except Exception as e:
            logging.error(f"Unable to delete temporary template path {template.template_path} because: " + str(e))
            raise

async def get_latex_template(info: LatexTemplateInfo, variables: list[LatexVariableInfo]) -> bytes:
    """
    Returns the template bytes for the compiled pdf usign given variables.
    """
    engine = RegexTemplateEngine()
    compiler = LatexCompiler()

    try:
        temp_template = engine.add_variable_values_to_template(info, **{
            x.name: x.value for x in variables 
        })
        pdf_path = await compiler.compile(temp_template)
        pdf_path = Path(pdf_path)
        return pdf_path.read_bytes()
    finally:
        try:
            shutil.rmtree(temp_template.template_path)
        except Exception as e:
            logging.error(f"Unable to delete temporary template path {temp_template.template_path} because: " + str(e))
            raise
