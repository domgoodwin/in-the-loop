# in-the-loop


## ai/summarizer

- Put model ./ai/summarizer/files/models/cnndm_bertsum_classifier_best.py 
- Install pip dependencies
- Run server.js
- Call POST localhost:5000/summary

```
python server.py
curl -X POST localhost:5000/summary -d '{"articles" : ["articlecontent"] }'
```

### Docker
```
docker build -t d0m182/in-the-loop-summary:$VERSION .

docker pull d0m182/in-the-loop-summary
docker run -it -p 8080:5000 d0m182/in-the-loop-summary
curl -X POST localhost:5000/summary -d '{"articles" : ["articlecontent"] }'
```

## ai/qa

- Put model ./ai/qa/files/models/out_model.ckpt-10859.data-00000-of-00001
- Install pip dependencies
- Run server.js
- Call POST localhost:5000/qa

```
python server.py
curl -X POST localhost:80/qa -d '{"data": [{"questions": ["Who won the election in 1997?"],"context": "Tony Blair was elected in 1997"}]}' -H "Content-Type: application/json"
```

### Docker
```
docker build -t d0m182/in-the-loop-qa:$VERSION .

docker pull d0m182/in-the-loop-qa
docker run -p 8081:5000 -it d0m182/in-the-loop-qa:$VERSION
curl -X POST localhost:8081/qa \
    -d '{"data": [{"questions": ["Who won the election in 1997?"],"context": "Tony Blair was elected in 1997"}]}' \
    -H "Content-Type: application/json"

```

## web-ui

### Development
``` bash
npm install
npm run devstart
```

### Docker image

``` bash
cd web-ui
docker build -t itl-web-ui .
docker run -p 8080:3000 -d itl-web-ui
```

### Overview
 - _/bin/www_ - app entrypoint
 - _/app.js_ - creates express server
 - _/routes/_ -  routes for the app
 - _/views/_ - pug template files
