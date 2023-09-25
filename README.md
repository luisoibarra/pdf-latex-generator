# PDF Latex Generator

Small and simple PDF generator based on latex templates.

## Use Case

Make a microservice for PDF generation.

## Usage

**Docker**

Build the docker image and start the container with this command:

`docker run -it --rm -p 8000:8000 pdf-latex-generator:1.0`

**Dev container**

Run `uvicorn app.main:app`

### Swagger

To see swagger documentation go to `http://localhost:8000/docs` once the container is started.

## PDF Template

A pdf template is a folder with all the files needed to compile a latex pdf. 

### Template requirements

- The template must provide a `template.tex` file in the template's root folder.
- The variables in the templates must have the following format `{{VariableName}}`.
- The template must provide all the file for compiling the pdf using **pdflatex** tool.

### Add templates

Copy the template to `app/latex/templates/` or use docker's volumes.
