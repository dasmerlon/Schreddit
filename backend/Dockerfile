FROM python:3.9

COPY . .

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry install 

WORKDIR /app

EXPOSE 8000

CMD [ "poetry" , "run", "./main.py" ]