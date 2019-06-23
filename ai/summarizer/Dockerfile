FROM python:3

WORKDIR /usr/src/app

RUN pip install numpy
RUN pip install torch torchvision
RUN pip install jmespath nltk mkl multiprocess olefile Pillow protobuf pycparser pyrouge python-dateutil pytorch-pretrained-bert s3transfer six tensorboardX tqdm urllib3 wincertstore
RUN pip install flask
RUN python -c "import nltk; nltk.download('punkt');"

COPY . .

# EXPOSE 5000

RUN python main.py

RUN rm ./files/models/cnndm_bertsum_classifier_best.pt

CMD [ "python", "./server.py" ]