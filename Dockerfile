FROM python:3.9 as fastapi
 
WORKDIR /crypto
 
COPY ./requirements.txt /crypto/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /crypto/requirements.txt
 
COPY ./src /crypto/src

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "80"]

FROM python:3.9 as scheduler

WORKDIR /crypto

COPY ./requirements.txt /crypto/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /crypto/requirements.txt

COPY ./src/executors/eda/script.py /crypto/src/executors/eda/script.py
COPY ./src/log /crypto/src/log

CMD ["python", "-m", "src.executors.eda.script"]
