import webapp2
import json
import logging as log

from google.appengine.ext import ndb
from google.appengine.api import users

from models import UserModel


class ListHandler(webapp2.RequestHandler):

  def get(self):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      entities = UserModel().list()
      
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
      is_admin = users.is_current_user_admin()
      
      response = {}
      
      entity = UserModel(id=user_id).get_by_id(user_id)
      if "to_dict" in dir(entity):
        response['success'] = True
        response['entity'] = entity.to_dict()
        response['entity']['admin'] = is_admin
        
        self.response.set_status(200)
        self.response.write(json.dumps(response))
      else:
        self.response.set_status(404)
        response['success'] = True
        response['message'] = "User does not exist."
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


  def put(self):
    try:
      user = users.get_current_user()

      self.response.headers['Content-Type'] = 'text/json'

      new_user = UserModel(
        id    = user.user_id(),
        name  = user.nickname(),
        email = user.email(),
        address = "Not available"
      )
      if new_user.has_valid_email():
        result = new_user.put()
        if result:
          user_a = {}
          user_a['entity'] = result.get().to_dict()
          user_a['entity']['id'] = user.user_id()
          user_a['success'] = True
          self.response.set_status(201)
          self.response.write(json.dumps(user_a))
      else:
        self.response.set_status(404)
        self.response.write(json.dumps( {"success": False, "message": "Invalid email address" } ))
    
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

      new_user = UserModel(
        id    = user_id,
        name  = jdata['name'],
        email = jdata['email'],
        address = jdata['address']
      )
      if new_user.has_valid_email():
        result = new_user.put()
        if result:
          user_a = {}
          user_a['entity'] = result.get().to_dict()
          user_a['entity']['id'] = user_id
          user_a['success'] = True
          self.response.set_status(201)
          self.response.write(json.dumps(user_a))
      else:
        self.response.set_status(404)
        self.response.write(json.dumps( {"success": False, "message": "Invalid email address" } ))
    
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

  def delete(self,id):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      #user = users.get_current_user()
      #user_id = user.user_id()

      if not id:
        self.response.set_status(404)
        self.response.write("{\"id value missing from url. aborted delete.\"}")
        return

      try:

        entity = UserModel(id=id).get_by_id(id)
        if "key" in dir(entity):
          entity.key.delete()
          self.response.set_status(200)
          self.response.write(json.dumps( {"success": True, "entity": { "id": id } } ))
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


class URLSHandler(webapp2.RequestHandler):

  def get(self):
    urls = {}
    urls['login'] = users.create_login_url('/')
    urls['logout'] = users.create_logout_url('/')
    self.response.set_status(200);
    self.response.write(json.dumps(urls))