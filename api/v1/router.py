import webapp2

API_VERSION = 'v1'

def handler(partial):
  return 'api' + '.' + API_VERSION + '.' + partial


route = webapp2.WSGIApplication([

  # User
  (r'/api/v1/user',                       handler('users.ListHandler')),
  (r'/api/v1/user/view',                  handler('users.ViewHandler')),
  (r'/api/v1/user/create',                handler('users.CreateUpdateHandler')),
  (r'/api/v1/user/update',                handler('users.CreateUpdateHandler')),
  (r'/api/v1/user/delete/(.*)',           handler('users.DeleteHandler')),
  (r'/api/v1/user/urls',                  handler('users.URLSHandler')),
  
  # PRODUCTS
  (r'/api/v1/products',                   handler('products.ListHandler')),
  (r'/api/v1/products/view/(.*)',         handler('products.ViewHandler')),
  (r'/api/v1/products/create',            handler('products.CreateHandler')),
  (r'/api/v1/products/update/(.*)',       handler('products.UpdateHandler')),
  (r'/api/v1/products/delete/(.*)',       handler('products.DeleteHandler')),

  # Manufacturer
  (r'/api/v1/manufacturer',               handler('manufacturer.ListHandler')),
  (r'/api/v1/manufacturer/view/(.*)',     handler('manufacturer.ViewHandler')),
  (r'/api/v1/manufacturer/create',        handler('manufacturer.CreateHandler')),
  (r'/api/v1/manufacturer/update/(.*)',   handler('manufacturer.UpdateHandler')),
  (r'/api/v1/manufacturer/delete/(.*)',   handler('manufacturer.DeleteHandler')),

  # Cart
  (r'/api/v1/cart',                       handler('cart.ListHandler')),
  (r'/api/v1/cart/view',                  handler('cart.ViewHandler')),
  (r'/api/v1/cart/create',                handler('cart.CreateUpdateHandler')),
  (r'/api/v1/cart/update',                handler('cart.CreateUpdateHandler')),
  (r'/api/v1/cart/delete',                handler('cart.DeleteHandler')),

  # Orders
  (r'/api/v1/orders',                     handler('order.ListHandler')),
  (r'/api/v1/orders/list',                handler('order.AdminListHandler')),
  (r'/api/v1/orders/view/(.*)',           handler('order.ViewHandler')),
  (r'/api/v1/orders/create',              handler('order.CreateHandler')),
  (r'/api/v1/orders/update/(.*)',         handler('order.UpdateHandler')),
  (r'/api/v1/orders/delete/(.*)',         handler('order.DeleteHandler')),



  (r'/api/v1/.*',                     handler('docs.DefaultHandler'))
], debug=True)
