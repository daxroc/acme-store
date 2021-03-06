import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'Docs')
  ),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)


class DefaultHandler(webapp2.RequestHandler):

  def get(self):
    data = {"api": {}}
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(data))
    
