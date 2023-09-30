from pydantic import BaseModel

class WordTemplateInfo(BaseModel):
    """
    DocxTemplateInfo
    """
    
    template_name: str
    """
    Template name: is the .docx file name without the trailing .docx.
    """

    template_path: str
    """
    Template path: Path of the template file in the file system.
    """
