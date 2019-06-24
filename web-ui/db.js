var pgp = require('pg-promise')(/* options */)
const db_addr = process.env.DB_ADDR || "127.0.0.1:5432"
const db_name = process.env.DB_NAME || "ai"
const db_password = process.env.DB_PASSWORD || "Immediate123"
const db_username = process.env.DB_USERNAME || "postgres"
var db = pgp('postgres://'+db_username+':'+db_password+'@'+db_addr+'/'+db_name)





exports.getSummaries = function () {
  try {
    return db.any('SELECT * FROM summaries ORDER BY date_added ASC');
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
    console.log(query)
    return db.one(query, [true]);
    // success
  } 
  catch(e) {
    console.log('ERROR:', error)
  }
}
