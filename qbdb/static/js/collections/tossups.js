define(['backbone',
        'jquery',
        'underscore',
        'models/tossup',
        'views/tossup'],
        function(Backbone, $, _, Tossup, TossupView) {

          var TossupCollection = Backbone.Collection.extend({
            model: Tossup,

            initialize: function() {
              console.log('init tossup collection')
            },


          });

          return TossupCollection;

        }
      );
