@ECHO off
TITLE 'app demo'
IF NOT EXIST .env (
    echo MYSQL_HOST=localhost >> .env
    echo MYSQL_PORT=3306 >> .env
    echo MYSQL_PASSWORD=insecure >> .env
    echo MYSQL_USER=root >> .env
    echo DB=demo >> .env
)
@WHERE python
IF %ERRORLEVEL% NEQ 0 (
    ECHO PYTHON NOT FOUND
    ECHO Please download and install Python @
    ECHO https://www.python.org/downloads/
    PAUSE
    EXIT
)
@WHERE docker
IF %ERRORLEVEL% NEQ 0 (
    ECHO DOCKER NOT FOUND
    ECHO Please download and install Docker @
    ECHO https://docs.docker.com/get-docker/
    PAUSE
    EXIT
)
IF NOT EXIST .venv (
    python -m venv .venv
)
CALL .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
docker-compose up -d
PAUSE
python -m src