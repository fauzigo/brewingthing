FROM python:3.8

# When running on raspberry pi 
# https://docs.linuxserver.io/faq
# Raspbian GNU/Linux 10 (buster)
# https://github.com/linuxserver/docker-papermerge/issues/4


# wget http://ftp.us.debian.org/debian/pool/main/libs/libseccomp/libseccomp2_2.5.3-2_armhf.deb
# sudo dpkg -i libseccomp2_2.5.3-2_armhf.deb
# more info for new version
# http://ftp.us.debian.org/debian/pool/main/libs/libseccomp/

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install pipenv

WORKDIR /usr/src/app
COPY app/ .
RUN pipenv install

ENV FLASK_APP main.py

CMD [ "pipenv", "run", "gunicorn", "-w", "4", "-b", ":9000", "main:app" ]

# should you decide to go public
# sudo apt-get install certbot
# sudo certbot certonly -d my-server-domain-name.com -n --standalone
# mkdir /home/pi/certs
# sudo cp /etc/letsencrypt/live/my-server-domain-name.com/fullchain.pem /home/pi/certs
# sudo cp /etc/letsencrypt/live/my-server-domain-name.com/privkey.pem /home/pi/certs/
# sudo chown pi:pi /home/pi/certs/*
#CMD [ "pipenv", "run", "gunicorn", "-w", "4", "-b", ":443", "--certfile", "/certs/fullchain.pem", "--keyfile", "/certs/privkey.pem", "hello:app" ]
