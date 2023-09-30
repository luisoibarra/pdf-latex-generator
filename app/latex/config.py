from pathlib import Path


class LatexConfig:
    # Default directory target to copy a generated template with the variables updated 
    TEMP_TEMPLATE_DIR = (Path(__file__).parent / "temp").resolve()
    # Default directory for storing latex templates 
    TEMPLATE_DIR = (Path(__file__).parent / "templates").resolve()
    
    # Prefix for variable in template
    VARIABLE_NAME_PREFIX = r"{{"
    # Suffix for variable in template
    VARIABLE_NAME_SUFFIX = r"}}"
    
    # Default file to target when compiling a latex template
    DEFAULT_TEMPLATE_TEX_FILENAME = "template.tex"
    # Default file name when compiling to pdf. Must be the same as DEFAULT_TEMPLATE_TEX_FILENAME but with .pdf
    DEFAULT_TEMPLATE_PDF_FILENAME = "template.pdf"

    # Command to compile a latex template
    COMMAND_COMPILE_LATEX = ["pdflatex"]

class WordConfig:
    # Default directory target to copy a generated template with the variables updated 
    TEMP_TEMPLATE_DIR = (Path(__file__).parent / "temp").resolve()
 
    TEMPLATE_DIR = (Path(__file__).parent / "templates").resolve()

    # Command to compile a docx template first part
    COMMAND_CONVERT_DOC_PDF_PART_1 = [
        "libreoffice", 
        "--headless", 
        "--convert-to", 
        "pdf", 
        # Doc to convert path goes here when building the command
    ]

    # Command to compile a docx template second part after the document
    COMMAND_CONVERT_DOC_PDF_PART_2 = [
        "--outdir",
    ]

    # Valid template suffixes for Word templates
    VALID_WORD_TEMPLATE_SUFFIX = [".docx"]
