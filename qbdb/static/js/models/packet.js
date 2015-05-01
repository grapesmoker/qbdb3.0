define(['backbone', 'jquery', 'underscore'],
  function(Backbone, $, _) {
    var Packet = Backbone.Model.extend({
      initialize: function() {

      },

      defaults: {

      },

      urlRoot: '/packet'

    });

    return Packet;
  }
);
