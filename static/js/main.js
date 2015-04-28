'use strict';

require.config({
  shim: {
    bootstrap: {
      deps: ['jquery'],
      exports: 'jquery'
    }
  },
  paths: {
    jquery: '../jquery/dist/jquery',
    backbone: '../backbone/backbone',
    underscore: '../underscore/underscore',
    bootstrap: '../bootstrap/dist/js/bootstrap',
    tossupView: './views/tossup',
    tossupModel: './models/tossup',
    tossupCollection: './collections/tossups',
    tossupCollectionView: './views/tossups',
    text: '../text/text'
  }
});

require([
  'backbone',
  'jquery',
  'underscore',
  'tossupView',
  'tossupModel',
  'tossupCollection',
  'tossupCollectionView'
], function(Backbone, $, _, TossupView, Tossup,
            TossupCollection, TossupCollectionView) {
  $(function() {

    console.log('init');
    console.log(Tossup);

    var tu = new Tossup;
    var tu_collection = new TossupCollection;
    tu_collection.add(tu)
    var tu_coll_view = new TossupCollectionView(tu_collection);

  })
})
