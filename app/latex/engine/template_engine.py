from io import BytesIO
from typing import Any, Optional
from app.latex.config import LatexConfig, WordConfig
from app.latex.engine.model.inline_latex_image import InlineLatexImage
from app.latex.exceptions.latex_exception import LatexEngineException
from app.latex.exceptions.word_exception import WordEngineException
from app.latex.models.compile_variable_info import DATA_VARIABLE_TYPE, IMAGE_VARIABLE_TYPE, JSON_VARIABLE_TYPE, CompileVariableInfo, DataVariableInfo, ImageVariableInfo
from app.latex.models.template_info import TemplateInfo
import random
import base64
from pathlib import Path
import shutil
import jinja2
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import matplotlib.pyplot as plt

def handle_data_variables(variables: list[CompileVariableInfo]) -> list[CompileVariableInfo]:
    """
    Convert the data variables into images.
    """
    images = []
    for var in [x for x in variables if x.type == DATA_VARIABLE_TYPE]:
        if isinstance(var.value, DataVariableInfo):
            data_var = var.value
            plt.plot(data_var.data)
            if data_var.x_label:
                plt.xlabel(data_var.x_label)
            if data_var.y_label:
                plt.ylabel(data_var.y_label)
            if data_var.title:
                plt.title(data_var.title)
            
            bio = BytesIO()
            plt.savefig(bio, format="png")
            bio.seek(0)
            my_base64_jpgData = base64.b64encode(bio.read()).decode()
            plt.close()

            images.append(CompileVariableInfo(name=var.name, type=IMAGE_VARIABLE_TYPE, value=ImageVariableInfo(base64_image=my_base64_jpgData, width=None, height=None)))
        else:
            raise ValueError(f"Value of variable {var.name} of type {DATA_VARIABLE_TYPE} is not DataVariableInfo")

    return [x for x in variables if x.type != DATA_VARIABLE_TYPE] + images

def handle_image_variables(template: TemplateInfo, new_temp_template_path: Path, name_tail: str, variables: list[CompileVariableInfo], doc: Optional[DocxTemplate]=None) -> list[CompileVariableInfo]:
    # Copy the template content into new folder
    new_temp_template_path.mkdir(parents=True)
    shutil.copytree(template.template_path,
                    new_temp_template_path, dirs_exist_ok=True)

    # Creating image variables
    image_variables = [x for x in variables if x.type == IMAGE_VARIABLE_TYPE]
    temp_template_image_path = new_temp_template_path / f"image_temp_{name_tail}"
    temp_template_image_path.mkdir()

    new_image_variables = []
    for image in image_variables:
        if isinstance(image.value, ImageVariableInfo):
            # Create new file for image
            temp_template_image_file_path = temp_template_image_path / (f"{image.name}.{LatexConfig.DEFAULT_IMAGE_EXTENSION}")
            temp_template_image_file_path.touch(exist_ok=False)
            # Decode image and put the content on the file
            temp_template_image_file_path.write_bytes(base64.b64decode(image.value.base64_image))
            # Add new variable with the path to the image
            if doc is not None:
                # Docx image
                image_options = {
                    name: Mm(value) 
                        for name, value in [
                            ("width", image.value.width), 
                            ("height", image.value.height),
                        ] if value is not None
                }
                new_image_variables.append(CompileVariableInfo(name=image.name, type=JSON_VARIABLE_TYPE, value=InlineImage(doc, str(temp_template_image_file_path), **image_options)))
            else:
                # Latex image
                new_image_variables.append(CompileVariableInfo(name=image.name, type=JSON_VARIABLE_TYPE, value=str(InlineLatexImage(image.value, str(temp_template_image_file_path)))))
        else:
            raise ValueError(f"Value of variable {image.name} of type {IMAGE_VARIABLE_TYPE} is not ImageVariableInfo")
    
    variables = [x for x in variables if x.type == JSON_VARIABLE_TYPE] + new_image_variables

    return variables

class LatexTemplateEngine:
    def add_variable_values_to_template(self, template: TemplateInfo, variables: list[CompileVariableInfo]) -> TemplateInfo:
        """
        Read the template and creates a new template with all the variables added. All values for variables will be
        replaced by their string representation.

        template: Base template
        variables: Variables to change in the template with their values
        """
        name_tail = str(random.randint(0, 1 << 32))

        new_temp_template_path = Path(
            LatexConfig.TEMP_TEMPLATE_DIR, template.template_name + name_tail)
        new_template_info = TemplateInfo(
            template_name=template.template_name + name_tail, 
            template_path=str(new_temp_template_path),
        )

        if new_temp_template_path.exists():
            raise LatexEngineException(
                "Failed to create a new temporary template folder because already exists. Try again.")

        # Convert data variables into image variables
        variables = handle_data_variables(variables)

        # Convert image variables into json variables
        variables = handle_image_variables(template, new_temp_template_path, name_tail, variables)
        
        template_content_path = Path(
            new_temp_template_path, LatexConfig.DEFAULT_TEMPLATE_TEX_FILENAME)
        template_content = template_content_path.read_text()

        # Update template variables
        environment = jinja2.Environment()
        jinja_template = environment.from_string(template_content)
        template_content = jinja_template.render({v.name: v.value for v in variables})

        template_content_path.write_text(template_content)
        return new_template_info

class WordTemplateEngine:

    def add_variable_values_to_template(self, template: TemplateInfo, variables: list[CompileVariableInfo]) -> TemplateInfo:
        name_tail = str(random.randint(0, 1 << 32))

        # Creating temporary template
        new_temp_template_path = Path(WordConfig.TEMP_TEMPLATE_DIR, template.template_name + name_tail)
        new_template_info = TemplateInfo(
            template_name=template.template_name, 
            template_path = str(new_temp_template_path))
        
        if new_temp_template_path.exists():
            raise WordEngineException(
                "Failed to create a new temporary template because already exists. Try again.")
        
        doc = DocxTemplate(Path(new_template_info.template_path, WordConfig.DEFAULT_TEMPLATE_WORD_FILENAME))
        
        # Convert data variables into image variables
        variables = handle_data_variables(variables)

        # Convert image variables into json variables
        variables = handle_image_variables(template, new_temp_template_path, name_tail, variables, doc)
        
        # Render document
        doc.render({v.name: v.value for v in variables if v.type == JSON_VARIABLE_TYPE})
        doc.save(Path(new_template_info.template_path, WordConfig.DEFAULT_TEMPLATE_WORD_FILENAME))

        return new_template_info
