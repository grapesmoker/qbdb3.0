define(['backbone',
        'jquery',
        'underscore',
        'models/bonus',
        'views/bonus',
        'views/bonuses'],
        function(Backbone, $, _, Bonus, BonusView) {

          var BonusCollection = Backbone.Collection.extend({
            model: Bonus,

            initialize: function() {
              console.log('init bonus collection')
            },


          });

          return BonusCollection;

        }
      );
