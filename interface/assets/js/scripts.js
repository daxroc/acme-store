
var apiEntry = function(entry){ return "api/v1/"+entry};
var app = angular.module("AcmeStore", []);

/**
 * Manufacture Service
 */

app.service('ManufactureService', function($http, $log, $q){
  
  var srvc = this;

  this.getManufacturers = function(){
      return $http.get(apiEntry('manufacturer'))
        .then(
          function(response){
            srvc.manufacturers = response.data.entities;
            return response.data.entities;
          });
    };

  this.update = function(uuid,data){
    endpoint = 'manufacturer/update/'+uuid;
    $http.put(apiEntry(endpoint), data);
    srvc.manufacturers[uuid] = data;
  };


  this.save = function(data){
    $http.post(apiEntry('manufacturer/create'), data);
  };

  this.delete = function(uuid){
    $http.delete(apiEntry('manufacturer/delete/'+uuid));
    delete srvc.manufacturers[uuid];
  };
  
  this.getManufacturers();

});

/**
 * Order Service
 */
app.service('OrderService', function($http, $log, $q){
  
  var srvc = this;

  // Get Users Orders
  this.getAllUserOrders = function(){
      return $http.get(apiEntry('orders'))
        .then(
          function(response){
            srvc.orders = response.data.entities;
          });
    };

  // Get All Users Orders - Admin function
  this.getAdminOrders = function() {
    return $http.get(apiEntry('orders/list'))
      .then(
        function(response){
          srvc.all_orders = response.data.entities;
        });
  };

  this.createOrder = function(cart){
    return $http.post(apiEntry('orders/create'),cart)
      .then(function(response){
        srvc.getAllUserOrders();
        srvc.getAdminOrders();
      });
  };

  this.delete = function(uuid){
    $http.delete(apiEntry('orders/delete/'+uuid));
    delete srvc.orders[uuid];
    if(typeof srvc.all_orders != 'undefined'){
      delete srvc.all_orders[uuid];
    }
  };

  this.getAdminOrders();
  this.getAllUserOrders();

});

/**
 * User Service
 */
app.service('UserService', function($http, $log, $q){
  
  var srvc = this;
  var login_status = false;

  this.registerUser = function(){
    $http.put(apiEntry('user/create'));
  };

  this.getURLs = function(){
      return $http.get(apiEntry('user/urls'))
        .then(
          function(response){
            srvc.urls = response.data;
          });
    };

  this.getUser = function(){
      return $http.get(apiEntry('user/view'))
        .then(
          function(response){
            srvc.account = response.data.entity;
            srvc.login_status = true;
          }, 
          function(reason){
            if(reason.data.message === "User does not exist."){
              srvc.registerUser();
              srvc.getUser();
            }
          });
    };

  this.getAllUsers = function(){
    return $http.get(apiEntry('user'))
      .then(
        function(response){
          srvc.users = response.data.entities;
        }
      );
  };

  this.update = function(){
    console.log(this);
    $http.post(apiEntry('user/update'), this.account);
  }


  this.delete = function(uuid){
    endpoint = 'user/delete/'+uuid
    $http.delete(apiEntry(endpoint));
  };

  this.getUser();
  this.getURLs();


});



/**
 * Products Service
 */
app.service('ProductService', function($http, $log, $q){
  
  var srvc = this;

  this.getProducts = function(){
      return $http.get(apiEntry('products'))
        .then(
          function(response){
            srvc.products = response.data.entities
            return response.data.entities
          });
    };

  this.save = function(){
    $http.post(apiEntry('products/create'), this.product);
  };

  this.update = function(){
    endpoint = 'products/update/'+srvc.uuid
    $http.put(apiEntry(endpoint), srvc.product)
  };

  this.getProducts();

});


/**
 * Cart Service
 */
app.service('CartService', function($http, $log, $q){
  
  var srvc = this;
  srvc.cart = {"cart_items":[]};

  this.getCart = function(){
      return $http.get(apiEntry('cart/view'))
        .then(
          function(response){
            srvc.cart = response.data.entity
            return response.data.entity
          });
    };

  this.runningTotal = function(){
    var total = 0;
    if(typeof srvc.cart != 'undefined'){
      angular.forEach(srvc.cart.cart_items, function(item){
        total += item.qty * item.price;
      });
    }
    return total;
  };

  this.add_item = function(item){
    item.qty = 1;
    items = srvc.cart.cart_items
    if(typeof srvc.cart != 'undefined'){
      if( $.inArray(item, srvc.cart.cart_items) >=0){
        console.log("Item already in cart");
      }else{
        srvc.cart.cart_items.push(item);
      }
    }

  };

  this.update = function(){
    $http.put(apiEntry('cart/update'), srvc.cart);
  };

  this.empty = function(){
    srvc.cart.cart_items = [];
  };

  this.getCart();

});

// ------------------------ Controllers ---------------------
/**
 * Tab Controller
 */
app.controller('TabCtrl', function(){
  this.active_tab = 1;
  
  this.setTab = function(id){
    this.active_tab = id;
  };
  
  this.isSet = function(id){
    if(this.active_tab === id){
      return true;
    }
    return false;
  };

})


app.controller('CartCtrl', function($scope, CartService, OrderService, UserService){
  
  this.CartService = CartService;
  this.OrderService = OrderService;

  $scope.createOrder = function(cart){
    // Save, Create, Empty
    this.cart.CartService.update(); 
    this.cart.OrderService.createOrder(angular.copy(this.cart.CartService.cart));
    // this.cart.CartService.empty();
    // this.cart.CartService.update();
  };

  $scope.delete = function(item) {
    position = $.inArray(item, this.cart.CartService.cart.cart_items);
    this.cart.CartService.cart.cart_items.splice(position,1);
  };

});

app.controller('ProductCtrl', function($scope, ProductService){

  this.ProductService = ProductService;

  this.ProductService.new_product = {
    "name": "Change me",
    "product_id": 0,
    "manufacturer_id": 0,
    "qty": 0,
    "price": 0.00
  }

  $scope.save = function(){
    this.product.ProductService.save();
  };

  $scope.update = function(){
    console.log("UPDATE PRODUCT");
    this.product.ProductService.update();
    this.tab.setTab(1);
  };


});


app.controller("UserCtrl", function($scope, UserService){
  this.UserService = UserService;

  $scope.save = function(){
    this.user.UserService.update();
  };

  $scope.delete = function(uuid,user){
    this.users.UserService.delete(uuid);
    delete this.users.UserService.users[uuid];
  };

});

app.controller("CatalogCtrl", function($scope, ProductService, CartService){
  this.ProductService = ProductService;
  this.CartService = CartService;

  $scope.edit = function(uuid,data){
    console.log(this);
    this.catalog.ProductService.uuid = uuid;
    this.catalog.ProductService.product = data;
    this.tab.setTab("edit_product");
  };

});


/**
 * Order Controller
 */
app.controller("OrderCtrl", function($scope, OrderService){
  this.OrderService = OrderService;

  $scope.delete = function(uuid){
    this.orders.OrderService.delete(uuid);
  };

});


/**
 * Manufacturer Controller
 */
app.controller("ManufactureCtrl",function($scope, ManufactureService){
  
  this.ManufacturerService = ManufactureService;
  this.new_manufacturer = {
    "manufacturer_id": 1,
    "business_name": "ACME",
    "email": "example@example.com",
    "url": "http://acme.example.com",
    "phone": "+353 123MYANVIL"
  };

  $scope.save = function(){
    data = this.manufacture.new_manufacturer;
    this.manufacture.ManufacturerService.save(data);
  };

  $scope.update = function(){
    data = this.manufacture.new_manufacturer;
    uuid = this.manufacture.uuid;
    this.manufacture.ManufacturerService.update(uuid,data);
    this.tab.setTab(8);
  };

  $scope.edit = function(uuid, item){
    this.manufacture.uuid = uuid;
    this.tab.setTab(7);
    this.manufacture.new_manufacturer = item;
  };

  $scope.cancel = function(){this.tab.setTab(8);};

  $scope.delete = function(uuid){
    this.manufacture.ManufacturerService.delete(uuid);
  };

});
