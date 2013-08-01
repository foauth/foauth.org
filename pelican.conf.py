SITENAME = 'foauth.org'
AUTHOR = 'Marty Alchin'
SITEURL = 'https://foauth.org/blog'
TIMEZONE = 'America/Los_Angeles'

DEFAULT_PAGINATION = 10

ARTICLE_URL = '{slug}/'
ARTICLE_SAVE_AS = '{slug}/index.html'
FEED_ALL_ATOM = 'feed.rss'

PATH = 'blog/content'
OUTPUT_PATH = 'blog/output'
USE_FOLDER_AS_CATEGORY = False
DELETE_OUTPUT_DIRECTORY = True

MARKUP = ['md']
TYPOGRIFY = True
