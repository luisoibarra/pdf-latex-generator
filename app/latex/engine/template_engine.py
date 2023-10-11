from typing import Any
from app.latex.config import LatexConfig, WordConfig
from app.latex.exceptions.latex_exception import LatexEngineException
from app.latex.exceptions.word_exception import WordEngineException
from app.latex.models.compile_variable_info import IMAGE_VARIABLE_TYPE, JSON_VARIABLE_TYPE, CompileVariableInfo
from app.latex.models.word_template_info import WordTemplateInfo
from app.latex.models.latex_template_info import LatexTemplateInfo
import random
import base64
from pathlib import Path
import shutil
import jinja2
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm


class LatexTemplateEngine:
    def add_variable_values_to_template(self, template: LatexTemplateInfo, variables: list[CompileVariableInfo]) -> LatexTemplateInfo:
        """
        Read the template and creates a new template with all the variables added. All values for variables will be
        replaced by their string representation.

        template: Base template
        variables: Variables to change in the template with their values
        """
        name_tail = str(random.randint(0, 1 << 32))

        new_temp_template_path = Path(
            LatexConfig.TEMP_TEMPLATE_DIR, template.template_name + name_tail)
        new_template_info = LatexTemplateInfo(
            template_name=template.template_name + name_tail, 
            template_path=str(new_temp_template_path),
        )

        if new_temp_template_path.exists():
            raise LatexEngineException(
                "Failed to create a new temporary template folder because already exists. Try again.")

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
            # Create new file for image
            temp_template_image_file_path = temp_template_image_path / (f"{image.name}.{LatexConfig.DEFAULT_IMAGE_EXTENSION}")
            temp_template_image_file_path.touch(exist_ok=False)
            # Decode image and put the content on the file
            temp_template_image_file_path.write_bytes(base64.b64decode(image.value))
            # Add new variable with the path to the image
            new_image_variables.append(CompileVariableInfo(name=image.name, type=JSON_VARIABLE_TYPE, value=str(temp_template_image_file_path)))

        variables = [x for x in variables if x.type == JSON_VARIABLE_TYPE] + new_image_variables

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

    def add_variable_values_to_template(self, template: WordTemplateInfo, variables: list[CompileVariableInfo]) -> WordTemplateInfo:
        name_tail = str(random.randint(0, 1 << 32))

        # Creating temporary template
        new_temp_template_path = Path(WordConfig.TEMP_TEMPLATE_DIR, template.template_name + name_tail)
        new_template_info = WordTemplateInfo(
            template_name=template.template_name, 
            template_path = str(new_temp_template_path))
        
        if new_temp_template_path.exists():
            raise WordEngineException(
                "Failed to create a new temporary template because already exists. Try again.")
        
        doc = DocxTemplate(Path(new_template_info.template_path, WordConfig.DEFAULT_TEMPLATE_WORD_FILENAME))
        
        # Copy the template content into new folder
        new_temp_template_path.mkdir(parents=True)
        shutil.copytree(template.template_path,
                        new_temp_template_path, dirs_exist_ok=True)

        # Creating image variables
        image_variables = [x for x in variables if x.type == IMAGE_VARIABLE_TYPE]
        temp_template_image_path = new_temp_template_path / f"image_temp_{name_tail}"
        temp_template_image_path.mkdir()

        new_image_variables = {}
        for image in image_variables:
            # Create new file for image
            temp_template_image_file_path = temp_template_image_path / image.name
            temp_template_image_file_path.touch(exist_ok=False)
            # Decode image and put the content on the file
            temp_template_image_file_path.write_bytes(base64.b64decode(image.value))
            # Add new variable with the path to the image
            new_image_variables[image.name] = InlineImage(doc, str(temp_template_image_file_path))

        # Render document
        doc.render({**{v.name: v.value for v in variables if v.type == JSON_VARIABLE_TYPE}, **new_image_variables})
        doc.save(Path(new_template_info.template_path, WordConfig.DEFAULT_TEMPLATE_WORD_FILENAME))

        return new_template_info
