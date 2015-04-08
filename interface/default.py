import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)


class DefaultHandler(webapp2.RequestHandler):

  def get(self):
    data = {}

    user = users.get_current_user()

    if user:
        data['username'] = user.nickname()
        data['auth'] = {
          "url": users.create_logout_url('/'),
          "action": "logout"
        }
    else:
        data['username'] = 'guest'
        data['auth'] = {
          "url": users.create_login_url('/'),
          "action": "login"
        }

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(data))

    
app = webapp2.WSGIApplication([
  ('/products/.*', 'interface.products.router.route'),
  ('/.*', DefaultHandler),
], debug=True)
