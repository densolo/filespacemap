var webpack = require('webpack');
var WebpackDevServer = require('webpack-dev-server');
var config = require('../../webpack.config');

var express = require("express");
var serveStatic = require("serve-static");

var app  = express();
var port = 3000;
var portStatic = port + 2;

app.use(serveStatic(__dirname + "/../../assets"));
app.listen(portStatic);


var  devServer = new WebpackDevServer(webpack(config), {
  publicPath: config.output.publicPath,
  hot: true,
  historyApiFallback: true,
  proxy: {
    "assets" : "http://localhost:" + portStatic
  }
});

devServer.listen(port, 'localhost', function (err, result) {
  if (err) {
    return console.log(err);
  }
  console.log('Listening at http://localhost:3002/assets/html/index.html');
});
