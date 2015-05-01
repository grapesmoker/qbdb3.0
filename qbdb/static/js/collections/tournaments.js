define(['backbone',
        'jquery',
        'underscore',
        'models/tournament',
        'views/tournament'],
        function(Backbone, $, _, Tournament, TournamentView) {

          var TournamentCollection = Backbone.Collection.extend({
            model: Tournament,

            initialize: function() {
              console.log('init tournament collection')  
            },

            url: '/tournaments'

          });

          return TournamentCollection;

        }
      );
