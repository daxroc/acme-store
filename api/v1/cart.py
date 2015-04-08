import webapp2
import json
import logging as log

from google.appengine.ext import ndb
from google.appengine.api import users

from models import CartModel
from models import ItemModel


class ListHandler(webapp2.RequestHandler):

  def get(self):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      entities = CartModel().list()
      
      response = {"success": True, "entities":{}}

      for entity in entities.fetch():
        key_id = entity.key.id()
        response['entities'][key_id] = (entity.to_dict())

      self.response.write(json.dumps(response))

    except Exception, e: 
      # Should Log to console - exception message
      log.debug(e)
      self.response.write(
        json.dumps({
          "success": False, 
          "message": "ViewHandler Exception: " + e.message
      }))


class ViewHandler(webapp2.RequestHandler):

 def get(self):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      user = users.get_current_user()
      user_id = user.user_id()
      
      response = {}
      
      entity = CartModel(id=user_id).get_by_id(user_id)
      if "to_dict" in dir(entity):
        response['success'] = True
        response['entity'] = entity.to_dict()
        
        self.response.set_status(200)
        self.response.write(json.dumps(response))
      else:
        self.response.set_status(404)
        response['success'] = True
        response['message'] = "Cart does not exist."
        self.response.write(json.dumps(response))

    except Exception, e: 
      log.debug(e)
      self.response.set_status(404)
      self.response.write(
        json.dumps({
          "success": False, 
          "message": "ViewHandler Exception: " + e.message
      }))

class CreateUpdateHandler(webapp2.RequestHandler):

  # As Create/Update Cart should be idempotent
  # PUT verb just calls the post method
  def put(self):
    self.post()

  def post(self):
    log.info("create")
    try:
      
      user = users.get_current_user()
      user_id = user.user_id()

      self.response.headers['Content-Type'] = 'text/json'

      try:
        jdata = json.loads(self.request.body)
      except ValueError, e:
        log.debug(e)
        self.response.set_status(404)
        msg = {'success': False, 'message': "Failed to read JSON body"}
        self.response.write(json.dumps(msg))
        return

      cart_items = jdata['cart_items']
      new_cart = CartModel(
        id              = user_id,
        cart_items      = cart_items
      )
      
      result = new_cart.put()
      if result:
        entity = result.get().to_dict()
        entity['success'] = True
        self.response.set_status(201)
        self.response.write(json.dumps(entity))
    
    except users.UserNotFoundError, e:
      # Should never happen - just incase of solar flares
      log.debug('User was not found...')
    except Exception, e: 
      log.debug(e)
      self.response.set_status(404)
      self.response.write(
        json.dumps({
          "success": False, 
          "message": "CreateHandler Exception: " + e.message
      }))
    

class DeleteHandler(webapp2.RequestHandler):

  def delete(self):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      user = users.get_current_user()
      user_id = user.user_id()

      try:

        entity = CartModel(id=user_id).get_by_id(user_id)
        if "key" in dir(entity):
          entity.key.delete()
          self.response.set_status(200)
          self.response.write(json.dumps( {"success": True, "entity": { "id": user_id } } ))
        else:
          self.response.set_status(200)
          self.response.write(json.dumps( {"success": True, "message": "entity did not exist." } ))


      except AttributeError, e:

        log.debug(e)
        self.response.set_status(404)
        self.response.write(
        json.dumps({
          "success": False, 
          "message": "DeleteHandler Exception: " + e.message
        }))  
      
    except Exception, e: 
      # Should Log to console - exception message
      log.debug(e)
      self.response.set_status(404)      
      self.response.write(
        json.dumps({
          "success": False, 
          "message": "DeleteHandler Exception: " + e.message
      }))
