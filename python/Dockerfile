FROM python:3.7

RUN apt update
RUN apt install ffmpeg -y

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

#CMD [ "python", "./your-daemon-or-script.py" ]