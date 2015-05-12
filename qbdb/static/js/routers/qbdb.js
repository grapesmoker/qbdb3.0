define(['backbone',
        'jquery',
        'jqueryui',
        'underscore',
        'models/tournament',
        'views/tournament',
        'collections/tournaments',
        'views/tournaments',
        'models/packet',
        'views/packet',
        'views/search',
        'text!templates/dialog.html',
        'jquerycookie',
        'bootstrap'],
         function(Backbone, $, $ui, _, Tournament, TournamentView,
           TournamentCollection, TournamentCollectionView, Packet, PacketView,
           SearchView, Dialog) {

          var QBDBRouter = Backbone.Router.extend({
            routes: {
              'browse': 'browse',
              'search': 'search',
              'read': 'read',
              'tournament/:id': 'showTournament',
              'packet/:id': 'showPacket',
            },

            browse: function() {
              var tournaments = new TournamentCollection();
              var tourView = new TournamentCollectionView(tournaments);
            },

            search: function() {
              var el = $('#qbdb-contents')
              el.html('')
              var searchView = new SearchView({el: el})
              searchView.render()
              // el.html(searchView.render().el)
            },

            read: function() {
              var dialog = _.template(Dialog)({text: 'This feature is not available yet.',
                                               title: 'Unimplemented feature.'})

              $(dialog).modal('show')
            },

            showTournament: function(id) {
              var tournament = new Tournament;
              tournament.set('id', id)
              var tournamentView = new TournamentView({model: tournament});
            },

            showPacket: function(id) {
              var packet = new Packet;
              packet.set('id', id)
              var packetView = new PacketView({model: packet})
            },

            showTossup: function(id) {

            }

          });

          Backbone.history.start();

          return QBDBRouter;

        });
