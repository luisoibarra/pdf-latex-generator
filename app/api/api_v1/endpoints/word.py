from fastapi import APIRouter, Depends, HTTPException
import base64

from latex.dependency_injection import WordEngineService, WordTemplateInfoRepository
from latex.dto.compile_template_request_dto import CompileTemplateRequestDto
from latex.dto.compile_template_response_dto import CompileTemplateResponseDto
from latex.models.template_info import TemplateInfo

router = APIRouter()

@router.post("/")
async def compile_word_templates(
    compile_template_info: CompileTemplateRequestDto,
    template_repo: WordTemplateInfoRepository = Depends(WordTemplateInfoRepository),
    word_engine_service: WordEngineService = Depends(WordEngineService),
    ) -> CompileTemplateResponseDto:
    """
    Compiles the given template with the given variables.
    """
    template = template_repo.get_template_info_by_name(compile_template_info.template_name)
    if not template:
        raise HTTPException(404, detail=f"Template with name {compile_template_info.template_name} wasn't found.")
    pdf_bytes = await word_engine_service.get_compiled_pdf_bytes(template, compile_template_info.template_variables)
    return CompileTemplateResponseDto(base64_encoded_pdf=base64.b64encode(pdf_bytes))

@router.get("/templates")
def get_templates_info(template_repo: WordTemplateInfoRepository = Depends(WordTemplateInfoRepository)) -> list[TemplateInfo]:
    return template_repo.get_all_templates()

@router.get("/template/{name}")
def get_templates_info_by_name(name: str, template_repo: WordTemplateInfoRepository = Depends(WordTemplateInfoRepository)) -> TemplateInfo:
    template = template_repo.get_template_info_by_name(name)
    if not template:
        raise HTTPException(404, detail=f"Template with name {name} wasn't found.")
    return template