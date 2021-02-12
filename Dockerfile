FROM python:3.9

WORKDIR /usr/app

COPY . .

RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "src"]