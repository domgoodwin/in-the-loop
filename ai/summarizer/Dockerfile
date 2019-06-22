FROM python:3

WORKDIR /usr/src/app

# RUN apt-get update && apt-get upgrade && apt-get dist-upgrade && apt-get autoremove
# RUN apt-get -y install python3 python-pip 
# RUN apt-get -y install libc-dev curl
# RUN apt-get -y install build-essential
# RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py
RUN pip install numpy
RUN pip install torch torchvision
RUN pip install jmespath nltk mkl multiprocess olefile Pillow protobuf pycparser pyrouge python-dateutil pytorch-pretrained-bert s3transfer six tensorboardX tqdm urllib3 wincertstore
RUN pip install flask
RUN python -c "import nltk; nltk.download('punkt');"

COPY . .

# EXPOSE 5000

RUN python main.py

CMD [ "python", "./server.py" ]