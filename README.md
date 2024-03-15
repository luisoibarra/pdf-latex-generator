# PDF Latex Generator

REST PDF generator based on latex and word templates.

## Use Case

Make a microservice for PDF generation.

## Usage

Create an instance of the service by choosing one of these options.

**Docker:**

Build the docker image and start the container with this command:

- Default host and port (**0.0.0.0** and **8000**): `docker run -it --rm -p 8000:8000 pdf-generator:1.0`
- Custom host and port: `docker run -it --rm -p <INTERNAL_PORT>:<EXTERNAL_PORT> pdf-generator:1.0 --host <HOST> --port <INTERNAL_PORT>`
- More customization: Search for arguments that receive this command `python -m uvicorn main:app`

**Dev container (mostly for development):**

Build the docker image and start the dev container in VSCode then press F5 to start debugging.

### Swagger

To see swagger documentation go to `http://localhost:8000/docs` once the container is started.

### Example requests

- Word template example

```json
// POST http://localhost:8000/api/v1/word

{
	"template_name": "TestWordTemplate",
	"template_variables": [
		{
			"name": "title",
			"value": "Insomnia Call Title"
		},
		{
			"name": "body",
			"value": "First Line From Insomnia"
		},
		{
			"name": "test_image",
			"type": "image",
			"value": {
				"base64_image": "<BASE 64 PNG IMAGE>",
				"width": 100,
				"height": 100
			}
		}
	]
}
```

- Latex template example

```json
// POST http://localhost:8000/api/v1/latex

{
	"template_name": "LaTeXTemplates_minimal-memo_v1.0",
	"template_variables": [
		{
			"name": "title",
			"value": "Insomnia Call Title"
		},
		{
			"name": "first_line",
			"value": "First Line From Insomnia"
		},
		{
			"name": "test_image",
			"type": "image",
			"value": {
				"base64_image": "<BASE 64 PNG IMAGE>",
				"width": 100,
				"height": 100
			}
		}
	]
}
```

## PDF Template

The service supports two kinds of templates:

- Latex templates: Folder with all the files needed to compile latex to pdf.
- Word templates: Folder containing a template docx file with markup language.

### General requirements

- Images must be PNG encoded in base64.
- Image sizes will be in millimeters.

### Latex template requirements

For handling templates the service uses [jinja engine](https://pypi.org/project/Jinja2/).

- The template must provide a `template.tex` file in the template's root folder.
- The variables in the templates must follow the standard [jinja format](https://jinja.palletsprojects.com/en/3.1.x/).
- The template must provide all the file for compiling the pdf using **pdflatex** tool.

### Word template requirements

- The template must provide a `template.docx` file in the template's root folder.
- The services uses [libreoffice](https://www.libreoffice.org/) and [docxtpl](https://pypi.org/project/docxtpl/) to build to pdf and replace tags.
  - Need to see the limitations of these tools when building templates.
  - For templates examples for [docxtpl](https://github.com/elapouya/python-docx-template/tree/master) see [here](https://github.com/elapouya/python-docx-template/tree/master/tests/templates)
- The variables in the templates must have a [jinja2](https://pypi.org/project/Jinja2/) format specified in docxtpl [documentation](https://docxtpl.readthedocs.io/en/latest/#jinja2-like-syntax)

### Add templates

Copy the template to `app/latex/templates/` or use docker's volumes.
