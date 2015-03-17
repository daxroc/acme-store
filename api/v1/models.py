import logging as log
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


class CartModel(ndb.Model):
  user              = ndb.UserProperty()
  cart_id           = ndb.IntegerProperty()
  cart_items        = ndb.StructuredProperty()
  cart_total        = ndb.StringProperty()

  def _pre_put_hook(self):
    log.info("CartModelPrePutHook")


class CartItemModel(ndb.Model):
  item_id           = ndb.IntegerProperty()
  product_id        = ndb.IntegerProperty()
  qty               = ndb.IntegerProperty()
  price             = ndb.FloatProperty()


class OrderModel(ndb.Model):
  user               = ndb.UserProperty()
  order_id           = ndb.IntegerProperty()
  order_items        = ndb.StructuredProperty()
  order_total        = ndb.StringProperty()


class OrderItemModel(ndb.Model):
  item_id           = ndb.IntegerProperty()
  product_id        = ndb.IntegerProperty()
  qty               = ndb.IntegerProperty()
  price             = ndb.FloatProperty()