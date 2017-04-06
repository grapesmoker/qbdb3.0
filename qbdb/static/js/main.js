window.$ = window.jQuery = require('jquery');
global.jQuery = require('jquery');
//var $ = require('jquery');
var bs = require('bootstrap');
var Backbone = require('backbone');
var _ = require('underscore');
var QBDBRouter = require('routers/qbdb');

var jquerycookie = require('jquery.cookie');

$(function() {

    // set up the custom header for csrf tokens
    var csrf = $.cookie('csrftoken');
    $.ajaxSetup({
      headers: {
        "X-CSRFToken": csrf
      }
    });

    var qbdbRouter = new QBDBRouter();

});

