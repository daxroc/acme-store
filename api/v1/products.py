import webapp2
import pprint
import json
import logging as log

from google.appengine.ext import ndb

from models import ProductModel


class ListHandler(webapp2.RequestHandler):

  def get(self):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      entities = ProductModel().list()
      
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
          "message": "ProductsViewHandler Exception: " + e.message
      }))


class ViewHandler(webapp2.RequestHandler):

 def get(self, id):
    try:

      self.response.headers['Content-Type'] = 'text/json'

      if not id:
        self.response.set_status(404)
        self.response.write("{\"id value missing from url. aborted update.\"}")
        return

      entity = ProductModel(id=id).get_by_id(int(id))
      response = {}
      response['success'] = True
      response['entity'] = {
        'id':               id,
        'product_id':       entity.product_id,
        'manufacturer_id':  entity.manufacturer_id,
        'name':             entity.name,
        'qty':              entity.qty
      }

      self.response.set_status(200)
      self.response.write(json.dumps(response))

    except Exception, e: 
      log.debug(e)
      self.response.set_status(404)
      self.response.write(
        json.dumps({
          "success": False, 
          "message": "ProductsViewHandler Exception: " + e.message
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
    
      new_product = ProductModel(
        product_id=jdata['product_id'],
        manufacturer_id=jdata['manufacturer_id'],
        name=jdata['name'],
        qty=jdata['qty'] or 0
      )
      
      result = new_product.put()
      
      if result:
        entity = result.get()
        data = {}
        data['success'] = True
        data['entity'] = {
          "id":               new_product.key.id(),
          "product_id":       entity.product_id,
          "manufacturer_id":  entity.manufacturer_id,
          "name":             entity.name,
          "qty":              entity.qty
        }
        self.response.set_status(201)
        self.response.write(json.dumps(data))
    
    except Exception, e: 
      log.debug(e)
      self.response.set_status(404)
      self.response.write(
        json.dumps({
          "success": False, 
          "message": "ProductsCreateHandler Exception: " + e.message
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
    
      entity = ProductModel(id=int(id)).get_by_id(int(id))
      
      entity.product_id           = jdata['product_id']
      entity.manufacturer_id      = jdata['manufacturer_id']
      entity.name = jdata['name'] = jdata['name']
      entity.qty = jdata['name']  = jdata['qty']
      
      result = entity.put()

      if result:
        rdata = {}
        rdata['success'] = True
        rdata['entity'] = {
          "product_id":       entity.product_id,
          "manufacturer_id":  entity.manufacturer_id,
          "name":             entity.name,
          "qty":              entity.qty
        }
        self.response.set_status(200)
        self.response.write(json.dumps(rdata))
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
        self.response.set_status(404)
        self.response.write("{\"id value missing from url. aborted delete.\"}")
        return

      try:

        entity = ProductModel(id=int(id)).get_by_id(int(id)).key.delete()
        self.response.set_status(200)
        self.response.write(json.dumps( {"success": True, "entity": { "id": id } } ))

      except AttributeError, e:

        log.debug(e)
        self.response.set_status(404)
        self.response.write(
        json.dumps({
          "success": False, 
          "message": "ProductsDeleteHandler Exception: " + e.message
        }))  
      
    except Exception, e: 
      # Should Log to console - exception message
      log.debug(e)
      self.response.set_status(404)      
      self.response.write(
        json.dumps({
          "success": False, 
          "message": "ProductsDeleteHandler Exception: " + e.message
      }))
