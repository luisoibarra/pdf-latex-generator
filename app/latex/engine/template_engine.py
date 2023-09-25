from typing import Any, Dict
from app.latex.config import LatexConfig
from app.latex.exceptions.latex_exception import LatexEngineException
from app.latex.models.latex_template_info import LatexTemplateInfo
import random
from pathlib import Path
import shutil
from abc import ABC, abstractmethod


class TemplateEngine(ABC):
    def add_variable_values_to_template(self, template: LatexTemplateInfo, **variables: Dict[str, Any]) -> LatexTemplateInfo:
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
        for var in variables:
            template_content = self._add_variable_to_template(
                var, str(variables[var]), template_content)
        template_content_path.write_text(template_content)

        return new_template_info

    @abstractmethod
    def _add_variable_to_template(self, variable: str, value: str, template_content: str) -> str:
        """
        Replace the variable with its value in the template.

        variable: Variable name to be replaced
        value: Variable value
        template_content: Current value of the template content

        return: The template with the replaced variable content
        """
        ...


class RegexTemplateEngine(TemplateEngine):
    def _add_variable_to_template(self, variable: str, value: str, template_content: str) -> str:
        return template_content.replace(LatexConfig.VARIABLE_NAME_PREFIX + variable + LatexConfig.VARIABLE_NAME_SUFFIX, value)
