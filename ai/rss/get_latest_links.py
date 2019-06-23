import feedparser # pip install feedparser

guardian_rss = 'https://www.theguardian.com/uk/rss'
bbc_rss = 'http://feeds.bbci.co.uk/news/rss.xml'
cnn_rss = 'http://rss.cnn.com/rss/edition_world.rss'
reuters_rss = 'http://feeds.reuters.com/reuters/UKdomesticNews'
tech_crunch_rss = 'http://feeds.feedburner.com/TechCrunch/'

feeds = 

feed = feedparser.parse(tech_crunch_rss)
for post in feed.entries:
  date = "(%d/%02d/%02d)" % (post.published_parsed.tm_year,\
    post.published_parsed.tm_mon, \
    post.published_parsed.tm_mday)
  title = post.title
  link = post.link
  print(link)
