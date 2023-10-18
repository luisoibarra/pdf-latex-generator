from pydantic import BaseModel

class TemplateInfo(BaseModel):
    template_name: str
    """
    Template name: is the folder name of the latex project.
    """

    template_path: str
    """
    Template path: Path of the template folder in the file system.
    """
