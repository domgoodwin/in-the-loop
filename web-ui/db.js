var pgp = require('pg-promise')(/* options */)
var db = pgp('postgres://postgres:test@127.0.0.1:5432/ai')





exports.getSummaries = function () {
  try {
    return db.any('SELECT * FROM summaries ORDER BY date_added ASC', [true]);
    // success
  } 
  catch(e) {
    console.log('ERROR:', error)
  }
}

exports.postSummary = function (title, content, summary, link) {
  try {
    console.log("POSTING "+summary)
    query = "INSERT INTO summaries(title, content, summary, date_added, link) "
    query += "values ('"+title+"', '"+content+"', '"+summary+"' ,now(), '"+link+"') RETURNING id;"
    db.one(query, [true]);
    // success
  } 
  catch(e) {
    console.log('ERROR:', error)
  }
}
