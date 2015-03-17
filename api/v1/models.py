import logging as log
import datetime

from google.appengine.ext import ndb

class ProductModel(ndb.Model):
  product_id        = ndb.IntegerProperty()
  manufacturer_id   = ndb.IntegerProperty()
  name              = ndb.StringProperty()
  qty               = ndb.IntegerProperty()
  cost              = ndb.FloatProperty()

  def list(cls):
    return cls.query()


class ManufacturerModel(ndb.Model):
  manufacturer_id   = ndb.IntegerProperty()
  business_name     = ndb.StringProperty()
  email             = ndb.StringProperty()
  url               = ndb.StringProperty()
  phone             = ndb.StringProperty()

  def list(cls):
    return cls.query()


class ItemModel(ndb.Model):
  product_id        = ndb.IntegerProperty()
  qty               = ndb.IntegerProperty()
  price             = ndb.FloatProperty()


class CartModel(ndb.Model):
  # id is user_id
  cart_items        = ndb.StructuredProperty(ItemModel, repeated=True)
  cart_total        = ndb.FloatProperty()

  def list(cls):
    return cls.query()

  def _pre_put_hook(self):
    self.cart_total = sum([ i.qty * i.price for i in self.cart_items])


class OrderModel(ndb.Model):
  # id is order #
  user_id = ndb.StringProperty()
  cart    = ndb.StructuredProperty(CartModel)
  created = ndb.StringProperty()
  updated = ndb.StringProperty()       

  def _pre_put_hook(self):
    self.cart.cart_total = sum([ i.qty * i.price for i in self.cart.cart_items])
    self.updated = datetime.datetime.now().strftime("%m-%d-%Y %H:%M")
    if self.created == None:
      self.created = self.updated



  def list(cls):
    return cls.query()
