from typing import Any
from app.latex.config import LatexConfig, WordConfig
from app.latex.exceptions.latex_exception import LatexEngineException
from app.latex.exceptions.word_exception import WordEngineException
from app.latex.models.word_template_info import WordTemplateInfo
from app.latex.models.latex_template_info import LatexTemplateInfo
import random
from pathlib import Path
import shutil
from docxtpl import DocxTemplate
import jinja2


class LatexTemplateEngine:
    def add_variable_values_to_template(self, template: LatexTemplateInfo, **variables: Any) -> LatexTemplateInfo:
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

        new_temp_template_path.mkdir(parents=True)
        shutil.copytree(template.template_path,
                        new_temp_template_path, dirs_exist_ok=True)

        template_content_path = Path(
            new_temp_template_path, LatexConfig.DEFAULT_TEMPLATE_TEX_FILENAME)
        template_content = template_content_path.read_text()

        # Update template variables
        environment = jinja2.Environment()
        jinja_template = environment.from_string(template_content)
        template_content = jinja_template.render(variables)

        template_content_path.write_text(template_content)
        return new_template_info

class WordTemplateEngine:

    def add_variable_values_to_template(self, template: WordTemplateInfo, **variables: Any) -> WordTemplateInfo:
        name_tail = str(random.randint(0, 1 << 32))

        doc = DocxTemplate(template.template_path)
        doc.render(variables)
        new_temp_template_path = Path(WordConfig.TEMP_TEMPLATE_DIR, template.template_name + "." + name_tail + ".docx")
        new_template_info = WordTemplateInfo(
            template_name=template.template_name, 
            template_path = str(new_temp_template_path))
        if new_temp_template_path.exists():
            raise WordEngineException(
                "Failed to create a new temporary template file because already exists. Try again.")

        doc.save(new_template_info.template_path)

        return new_template_info
