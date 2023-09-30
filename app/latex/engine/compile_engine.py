from app.latex.config import LatexConfig, WordConfig
from app.latex.exceptions.latex_exception import LatexEngineException
from app.latex.exceptions.word_exception import WordEngineException
from app.latex.models.word_template_info import WordTemplateInfo
from app.latex.models.latex_template_info import LatexTemplateInfo
from pathlib import Path
import asyncio
import logging


class LatexCompiler:

    async def compile(self, template: LatexTemplateInfo) -> str:
        """
        Compiles a latex template.

        Args:
            template: A LatexTemplateInfo object representing the template to compile.

        Raises:
            LatexEngineException: If the latex compilation fails with a non-zero exit code.

        Returns:
            The absolute path of the compiled pdf file.
        """
        value = await asyncio.create_subprocess_shell(
            # cd TEMPLATE_PATH && pdflatex template.tex
            " && ".join([
                f"cd {Path(template.template_path).resolve()}",
                " ".join(LatexConfig.COMMAND_COMPILE_LATEX + [LatexConfig.DEFAULT_TEMPLATE_TEX_FILENAME]),
            ]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await value.communicate()
        logging.info(
            f"Latex compilation process end with code {value.returncode}")
        if stderr:
            logging.error(f"Latex compilation process errors: {stderr}")
        if stdout:
            logging.debug(f"Latex compilation process output: {stdout}")
        if value.returncode != 0:
            raise LatexEngineException(
                f"Latex compilation failed with code {value.returncode}")
        return str(Path(template.template_path, LatexConfig.DEFAULT_TEMPLATE_PDF_FILENAME).resolve())


class WordCompiler:

    async def compile(self, template: WordTemplateInfo) -> str:
        """
        Compiles a word template.

        Args:
            template: A DocxTemplateInfo object representing the template to compile.

        Raises:
            WordEngineException: If the word compilation fails with a non-zero exit code.

        Returns:
            The absolute path of the compiled pdf file.
        """
        value = await asyncio.create_subprocess_shell(
            # cd TEMPLATE_PATH && pdflatex template.tex
            " && ".join([
                f"cd {Path(template.template_path).parent.resolve()}",
                " ".join(WordConfig.COMMAND_CONVERT_DOC_PDF_PART_1 + 
                         [template.template_path] + 
                         WordConfig.COMMAND_CONVERT_DOC_PDF_PART_2 + 
                         [str(Path(template.template_path).parent.resolve())]),
            ]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await value.communicate()
        logging.info(
            f"Word compilation process end with code {value.returncode}")
        if stderr:
            logging.error(f"Word compilation process errors: {stderr}")
        if stdout:
            logging.debug(f"Word compilation process output: {stdout}")
        if value.returncode != 0:
            raise WordEngineException(
                f"Word compilation failed with code {value.returncode}")
        temp_path = Path(template.template_path)
        return str(Path(temp_path.parent, temp_path.stem + ".pdf").resolve())
