# enconding: utf-8

import sys
import argparse
from workflow import Workflow

def main(wf):
  parser = argparse.ArgumentParser()
  parser.add_argument('query', nargs='?', default=None)
  args = parser.parse_args(wf.args)
  wf.save_password('apikey', args.query)

if __name__ == u"__main__":
  wf = Workflow()
  sys.exit(wf.run(main))
