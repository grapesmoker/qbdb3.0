'use strict';

require.config({
  shim: {
    bootstrap: {
      deps: ['jquery'],
      exports: 'jquery'
    },
  },
  paths: {
    jquery: '../jquery/dist/jquery',
    jqueryui: '../jquery-ui/jquery-ui',
    jquerycookie: '../jquery-cookie/jquery.cookie',
    backbone: '../backbone/backbone',
    underscore: '../underscore/underscore',
    bootstrap: '../bootstrap/dist/js/bootstrap',
    tossupView: './views/tossup',
    tossupModel: './models/tossup',
    tossupCollection: './collections/tossups',
    tossupCollectionView: './views/tossups',
    qbdbRouter: './routers/qbdb',
    text: '../requirejs-text/text'
  }
});

require([
  'backbone',
  'jquery',
  'underscore',
  'tossupView',
  'tossupModel',
  'tossupCollection',
  'tossupCollectionView',
  'qbdbRouter',
  'jquerycookie'
], function(Backbone, $, _, TossupView, Tossup,
            TossupCollection, TossupCollectionView, QBDBRouter) {
  $(function() {

    // set up the custom header for csrf tokens
    var csrf = $.cookie('csrftoken')
    $.ajaxSetup({
      headers: {
        "X-CSRFToken": csrf
      }
    });
    
    var qbdbRouter = new QBDBRouter;

  })
})
