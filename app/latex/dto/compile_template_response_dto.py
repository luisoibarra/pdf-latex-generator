from pydantic import BaseModel


class CompileTemplateResponseDto(BaseModel):
    base64_encoded_pdf: bytes
