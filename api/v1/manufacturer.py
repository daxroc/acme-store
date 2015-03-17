import webapp2
import pprint
import json
import logging as log

from google.appengine.ext import ndb

from models import ManufacturerModel


class ListHandler(webapp2.RequestHandler):

  def get(self):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      entities = ManufacturerModel().list()
      
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

      if not id:
        self.response.set_status(404)
        self.response.write("{\"id value missing from url. aborted update.\"}")
        return

      entity = ManufacturerModel(id=id).get_by_id(int(id))
      response = {}
      response['success'] = True
      response['entity'] = {
        "id":                 entity.key.id(),
        "manufacturer_id":    entity.manufacturer_id,
        "business_name":      entity.business_name,
        "email":              entity.email,
        "url":                entity.url,
        "phone":              entity.phone
      }

      self.response.set_status(200)
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
    try:
      
      self.response.headers['Content-Type'] = 'text/json'

      try:
        jdata = json.loads(self.request.body)
      except ValueError, e:
        log.debug(e)
        self.response.set_status(404)
        msg = {'success': False, 'message': "Failed to read JSON body"}
        self.response.write(json.dumps(msg))
        return
    
      new_manufacturer = ManufacturerModel(
        manufacturer_id   = jdata['manufacturer_id'],
        business_name     = jdata['business_name'],
        email             = jdata['email'],
        url               = jdata['url'],
        phone             = jdata['phone']
      )
      
      result = new_manufacturer.put()
      
      if result:
        entity = result.get()
        data = {}
        data['success'] = True
        data['entity'] = {
          "id":                 new_manufacturer.key.id(),
          "manufacturer_id":    entity.manufacturer_id,
          "business_name":      entity.business_name,
          "email":              entity.email,
          "url":                entity.url,
          "phone":              entity.phone
        }
        self.response.set_status(201)
        self.response.write(json.dumps(data))
    
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
    
      entity = ManufacturerModel(id=int(id)).get_by_id(int(id))
            
      entity.manufacturer_id   = jdata['manufacturer_id']
      entity.business_name     = jdata['business_name']
      entity.email             = jdata['email']
      entity.url               = jdata['url']
      entity.phone             = jdata['phone']
      
      result = entity.put()

      if result:
        rdata = {}
        rdata['success'] = True
        rdata['entity'] = {
          "id":                 entity.key.id(),
          "manufacturer_id":    entity.manufacturer_id,
          "business_name":      entity.business_name,
          "email":              entity.email,
          "url":                entity.url,
          "phone":              entity.phone
        }
        self.response.set_status(200)
        self.response.write(json.dumps(rdata))
    except AttributeError, e:
      log.debug(e)
      self.response.set_status(204)
      self.response.write(
        json.dumps({
          "success": False, 
          "message": "UpdateHandler Exception: " + e.message
      }))
    except Exception, e: 
      log.debug(e)
      self.response.set_status(404)
      self.response.write(
        json.dumps({
          "success": False, 
          "message": "UpdateHandler Exception: " + e.message
      }))
    

class DeleteHandler(webapp2.RequestHandler):

  def delete(self, id):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      if not id:
        self.response.set_status(404)
        self.response.write("{\"id value missing from url. aborted delete.\"}")
        return

      try:

        entity = ManufacturerModel(id=int(id)).get_by_id(int(id)).key.delete()
        self.response.set_status(200)
        self.response.write(json.dumps( {"success": True, "entity": { "id": id } } ))

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
