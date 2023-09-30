from pathlib import Path

from app.latex.models.compile_variable_info import CompileVariableInfo

from .dependency_injection import LatexEngineService, WordEngineService
from .models.word_template_info import WordTemplateInfo
from .models.latex_template_info import LatexTemplateInfo

async def test_latex_flow():
    engine = LatexEngineService()
    await engine.get_compiled_pdf_bytes(
        LatexTemplateInfo(
                template_name="LaTeXTemplates_minimal-memo_v1.0",
                template_path=str(Path(__file__, "..", "templates",
                                "LaTeXTemplates_minimal-memo_v1.0").resolve()),
            ), [
                CompileVariableInfo(name = "title", value="Template Test"),
                CompileVariableInfo(name = "first_line", value="TTHIS IS THE FIRST LINE OF THE BODY. PLACED BY TEMPLATE ENGINE"),
            ])

async def test_word_flow():
    engine = WordEngineService()
    await engine.get_compiled_pdf_bytes(
        WordTemplateInfo(
                template_name="TestWordTemplate",
                template_path=str(Path(__file__, "..", "templates",
                                "TestWordTemplate.docx").resolve()),
            ), [
                CompileVariableInfo(name = "title", value="Template Test"),
                CompileVariableInfo(name = "body", value="TTHIS IS THE FIRST LINE OF THE BODY. PLACED BY TEMPLATE ENGINE"),
            ])