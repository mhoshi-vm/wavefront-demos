FROM python

RUN apt-get update

ADD ./ /opt/hello-world
WORKDIR /opt/hello-world
RUN pip3 install -r requirements.txt

CMD [ "python", "/opt/hello-world/helloworld.py"]
