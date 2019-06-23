FROM python:3

WORKDIR /usr/src/app

RUN pip install tensorflow
# RUN pip install torch torchvision
# RUN pip install jmespath nltk mkl multiprocess olefile Pillow protobuf pycparser pyrouge python-dateutil pytorch-pretrained-bert s3transfer six tensorboardX tqdm urllib3 wincertstore
RUN pip install flask

COPY . .

WORKDIR /usr/src/app/bert


CMD [ "python", "server.py" ]