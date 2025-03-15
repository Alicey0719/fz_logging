FROM python:3.13.2

RUN useradd -ms /bin/bash fzlogger
USER fzlogger

COPY . /opt/app
WORKDIR /opt/app

RUN python -m pip install -r requirements.txt

CMD ["python", "device_logging.py"]