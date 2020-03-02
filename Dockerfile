FROM jupyter/scipy-notebook:latest

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY main.py .

ENTRYPOINT [ "python", "main.py"]
