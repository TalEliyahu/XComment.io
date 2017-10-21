var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000;


//app.use(bodyParser.urlencoded({ extended: true }));
//app.use(bodyParser.json());


var routes = require('./api/routes/cmntSyncRoute.js'); //importing route
routes(app); //register the route


app.listen(port);

console.log('todo list RESTful API server started on: ' + port);


