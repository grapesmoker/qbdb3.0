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
  'qbdbRouter'
], function(Backbone, $, _, TossupView, Tossup,
            TossupCollection, TossupCollectionView, QBDBRouter) {
  $(function() {

    console.log('init');

    /*var tu = new Tossup;
    var tu_collection = new TossupCollection;
    tu_collection.add(tu)
    var tu_coll_view = new TossupCollectionView(tu_collection);*/
    var qbdbRouter = new QBDBRouter;

  })
})
