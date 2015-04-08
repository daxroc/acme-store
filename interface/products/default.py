import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates')
  ),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)


class ProductDefaultHandler(webapp2.RequestHandler):

  def get(self):
    data = {}
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(data))
    

class ProductCreateHandler(webapp2.RequestHandler):

  def get(self):
    data = {}
    template = JINJA_ENVIRONMENT.get_template('create_product.html')
    self.response.write(template.render(data))
    
class ProductUpdateHandler(webapp2.RequestHandler):

  def get(self):
    data = {}
    template = JINJA_ENVIRONMENT.get_template('update_product.html')
    self.response.write(template.render(data))

class ProductDeleteHandler(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.write('Delete Product')
    



application = webapp2.WSGIApplication([
  (r'/products/create',       ProductCreateHandler),
  (r'/products/update/\d*',   ProductUpdateHandler),
  (r'/products/delete/\d*',   ProductDeleteHandler),
  (r'/products/.*',           ProductDefaultHandler),
], debug=True)
