# in-the-loop


## nlp-engine

`todo`

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