FROM danteev/texlive:2023-11-01

RUN mkdir /app
COPY app /app
WORKDIR /app

RUN apt update
RUN apt install python3.11-venv -y
RUN python -m venv .venv && .venv/bin/pip install -r requirements.txt
# RUN python -m venv /app/.venv && source /app/.venv/bin/activate && pip install -r requirements.txt
RUN apt install libreoffice -y

CMD ["/app/.venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
