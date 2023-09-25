FROM danteev/texlive:latest

RUN pip install fastapi && pip install "uvicorn[standard]" && pip install pydantic-settings

RUN mkdir /app
COPY app /app

WORKDIR /
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
