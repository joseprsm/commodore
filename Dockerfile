FROM python:3.10

COPY pyproject.toml .

COPY commodore commodore

RUN pip install .

ENTRYPOINT ["uvicorn", "commodore.app.main:app", "--reload"]