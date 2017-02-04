# encoding: utf-8

import sys
import argparse
import urllib
from xml.etree import ElementTree
from workflow import Workflow, ICON_WARNING, web, PasswordNotFound

basehref = 'https://www.goodreads.com'

def main(wf):
  parser = argparse.ArgumentParser()
  parser.add_argument('query', nargs='?', default=None)
  args = parser.parse_args(wf.args)

  try:
    apikey = wf.get_password('apikey')
  except PasswordNotFound:
    wf.add_item('Goodreads API key not set',
                'Please use grsetkey to set your Goodreads API key.',
                valid=False,
                icon=ICON_WARNING)
    wf.send_feedback()
    return 0

  query = args.query

  if query:
    for item in items(apikey, query, wf.logger):
      title = item['title']
      wf.add_item(title=title,
                  subtitle=u'Open ' + title + u' on goodreads.com',
                  uid=item['uid'],
                  arg=item['uid'],
                  valid=True)
  else:
    wf.add_item('Type in an author or a title')

  wf.send_feedback()

def items(apikey, query, logger):
  xml = get(apikey, query, logger)
  return map(toItem, xml.findall('.//work'))

def toItem(work):
  title = work.find('./best_book/title').text
  uid = work.find('./best_book/id').text
  return dict(title=title,
              uid=uid)

def get(apikey, query, logger):
  r = web.get(url(apikey, query))
  r.raise_for_status()
  logger.info(r.encoding)
  logger.info(r.mimetype)
  return ElementTree.fromstring(r.content)

def url(apikey, query):
  q = urllib.quote(query)
  return basehref + '/search/index.xml?key=' + apikey + '&q=' + q

if __name__ == u"__main__":
  wf = Workflow()
  sys.exit(wf.run(main))
