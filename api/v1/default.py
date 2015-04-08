import webapp2

class DefaultHandler(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.write("<h1>Hello API</h1>")
    
