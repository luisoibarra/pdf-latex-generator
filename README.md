# PDF Latex Generator

REST PDF generator based on latex and word templates.

## Use Case

Make a microservice for PDF generation.

## Usage

**Docker**

Build the docker image and start the container with this command:

`docker run -it --rm -p 8000:8000 pdf-latex-generator:1.0`

**Dev container (mostly for development)**

Build the docker image and start the dev container in VSCode then press F5 to start debugging.

### Swagger

To see swagger documentation go to `http://localhost:8000/docs` once the container is started.

## PDF Template

The service supports two kinds of templates:

- Latex templates: Folder with all the files needed to compile latex to pdf.
- Word templates: A docx file containing template markup language.

### Latex template requirements

- The template must provide a `template.tex` file in the template's root folder.
- The variables in the templates must have the following format `{{VariableName}}`.
- The template must provide all the file for compiling the pdf using **pdflatex** tool.

### Word template requirements

- The services uses [libreoffice]() and [docxtpl](https://pypi.org/project/docxtpl/) to build to pdf and replace tags.
  - Need to see the limitations of these tools when building templates.
  - For templates examples for [docxtpl](https://github.com/elapouya/python-docx-template/tree/master) see [here](https://github.com/elapouya/python-docx-template/tree/master/tests/templates)
- The variables in the templates must have a [jinja2](https://pypi.org/project/Jinja2/) format especified in docxtpl [documentation](https://docxtpl.readthedocs.io/en/latest/#jinja2-like-syntax)

### Add templates

Copy the template to `app/latex/templates/` or use docker's volumes.
