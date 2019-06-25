var express = require('express');
var router = express.Router();
var db = require('../db.js');
const request = require('request');

router.get('/summary', function(req, res, next) {
  res.render('summary', { title: 'Article summariser' });
});

router.post('/summary', function(req, res, next) {
  data = {}
  if (req.body.url){
    data = {articles : [{url: req.body.url}]};
  } else {
    var content = req.body.contents.replace(/\n/g, " ")
    content = content.replace(/\r/g, " ")
    content = content.replace(/\'/g, "")
    content = content.replace(/\"/g, "")
    content = content.replace(/\'/g, "")
    data = { articles:[content] }
  }

  const URL = process.env.SUMMARY_URL || "localhost"
  const PORT = process.env.SUMMARY_PORT || "30000"
  console.log("Creating summary for:")
  console.log(data)
  request('http://'+URL+':'+PORT+'/summary',{method: "POST", json: true, body: data}, (err, response, body) => {
    if (err) { return console.log(err); }
    // console.log(body);
    console.log(body);
    // res.send(`Creating summary for: ${content}`);
    res.render('summaryresponse', {summary: body.output[0].summary})
    url = req.body.url || "N/A"
    title = body.output[0].title || "N/A"
    db.postSummary(title, body.output[0].text.replace(/[^a-zA-Z ]/g, ""), body.output[0].summary, url)
    .then(function (data) {
      console.log(data)
    })
    .catch(function (error) {
      console.log('ERROR:', error)
    })
  });
  // res.send(`Creating summary for: ${req.body.contents}`);
});

router.get('/question', function(req, res, next) {
  // res.send('respond with a resource');
  res.render('question', { title: 'Article Q+A' });
});

router.post('/question', function(req, res, next) {
  console.log("Getting question answer")
  data = {}
  if (req.body.url){
    data = {data: [{questions: [ req.body.question ], url: req.body.url}]};
  } else {
    var content = req.body.contents.replace(/\n/g, " ")
    content = content.replace(/\r/g, " ")
    content = content.replace(/\'/g, "")
    content = content.replace(/\"/g, "")
    data = { data: [{questions: [ req.body.question ], context: content}]};
  }
  console.log("Sending data to qa server")
  console.log(data)
  const URL = process.env.QA_URL || "localhost"
  const PORT = process.env.QA_PORT || "30000"
  // data = { questions: [ req.body.question ], data:[{context: content, questions: [ req.body.question ] }] }
  // console.log(data)
  request('http://'+URL+':'+PORT+'/qa',{method: "POST", json: true, body: data}, (err, response, body) => {
    if (err) { return console.log(err); }
    console.log(body);
    // console.log(response);
    // // res.send(`Creating summary for: ${content}`);\
    questions = []
    answers = []
    for(var key in body) {
      questions.push(key)
      ans = ""
      if(body[key][0]) {
        ans = body[key][0]
      }
      else{ 
        ans = "/Not Found/"
      }
      answers.push(ans);
    }
    console.log(questions)
    console.log(answers)
    res.render('questionresponse', {questions: questions, answers: answers})
  });
  // res.send(`Creating summary for: ${req.body.contents}`);
});

router.get('/summaries', function(req, res, next) {
  db.getSummaries()
  .then(function (data) {
    console.log(data)
    res.render('summaries', {summaries: data})
  })
  .catch(function (error) {
    console.log('ERROR:', error)
  })
  
});

router.get('/', function(req, res, next) {
  res.render('summary', { title: 'Article summariser' });
});

module.exports = router;
