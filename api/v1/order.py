import webapp2
import json
import logging as log

from google.appengine.ext import ndb
from google.appengine.api import users

from models import OrderModel
from models import CartModel


class ListHandler(webapp2.RequestHandler):

  def get(self):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      user = users.get_current_user()
      user_id = user.user_id()

      entities = OrderModel(user_id=user_id).list()
      
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

 def get(self, id):
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

class CreateHandler(webapp2.RequestHandler):


  def post(self):
    log.info("create")
    try:
      
      user = users.get_current_user()
      user_id = user.user_id()

      self.response.headers['Content-Type'] = 'text/json'

      cart_entity = CartModel(id=user_id).get_by_id(user_id)
      log.info(cart_entity)
      if "to_dict" in dir(cart_entity):
        new_order = OrderModel(
          user_id    = user_id,
          cart  = cart_entity
        )
      else:
        self.response.set_status(404)
        self.response.write(json.dumps({
          "message": "Could not place order. No cart Found.",
          "success": False
        }))
        return
      
      result = new_order.put()
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
    
class UpdateHandler(webapp2.RequestHandler):

  def put(self, id):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      user = users.get_current_user()
      user_id = user.user_id()

      if not id:
        self.response.set_status(204)
        self.response.write("{\"id value missing from url. aborted update.\"}")
        return

      try:
        jdata = json.loads(self.request.body)
      except ValueError, e:
        log.debug(e)
        self.response.set_status(404)
        msg = {'success': False, 'message': "Failed to read JSON body"}
        self.response.write(json.dumps(msg))
        return
    
      entity = OrderModel(id=int(id)).get_by_id(int(id))
      
      entity.id        = id 
      entity.user_id   = user_id
      entity.cart      = jdata['cart']
      entity.created   = jdata['created'] 

      result = entity.put()

      if result:
        entity = result.get().to_dict()
        entity['success'] = True

        self.response.set_status(200)
        self.response.write(json.dumps(entity))

    except AttributeError, e:
      log.debug(e)
      self.response.set_status(204)
      self.response.write(
        json.dumps({
          "success": False, 
          "message": "ProductsUpdateHandler Exception: " + e.message
      }))
    except Exception, e: 
      log.debug(e)
      self.response.set_status(404)
      self.response.write(
        json.dumps({
          "success": False, 
          "message": "ProductsUpdateHandler Exception: " + e.message
      }))


class DeleteHandler(webapp2.RequestHandler):

  def delete(self, id):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      if not id:
        self.response.set_status(204)
        self.response.write("{\"id value missing from url. aborted update.\"}")
        return

      user = users.get_current_user()
      user_id = user.user_id()

      try:
        error = False
        entity = OrderModel(id=int(id)).get_by_id(int(id))
        if "key" in dir(entity):
          if user_id == entity.user_id:
            entity.key.delete()
            self.response.set_status(200)
            self.response.write(json.dumps( {"success": True, "entity": { "id": user_id } } ))
          else:
            error = True
            msg = "Not authorized to delete this record. Bad user!"    
        else:
          error = True
          msg = "Whahey it's like Jimmy Hoffa, No body... I mean entity found"

        if error:
          self.response.set_status(200)
          self.response.write(json.dumps( {"success": False, "message": msg } ))


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
