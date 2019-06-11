var express = require('express');
var router = express.Router();

router.get('/summary', function(req, res, next) {
  res.render('summary', { title: 'Article summariser' });
});

router.post('/summary', function(req, res, next) {
  res.send(`Creating summary for: ${req.body.contents}`);
});

router.get('/question', function(req, res, next) {
  // res.send('respond with a resource');
  res.render('question', { title: 'Article Q+A' });
});

router.post('/question', function(req, res, next) {
  res.send(`I will get your answer for ${req.body.question} from: ${req.body.contents}`);
});

module.exports = router;
