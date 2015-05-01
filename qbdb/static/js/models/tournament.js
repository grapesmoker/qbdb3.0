define(['backbone', 'jquery', 'underscore'],
  function(Backbone, $, _) {
    var Tournament = Backbone.Model.extend({
      initialize: function() {

      },

      defaults: {

      },

      urlRoot: '/tournament'

    });

    return Tournament;
  }
);
