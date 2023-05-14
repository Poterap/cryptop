 FROM python:3.9
 
WORKDIR /crypto
 
COPY ./requirements.txt /crypto/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /crypto/requirements.txt
 
COPY ./src /crypto/src

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "80"]