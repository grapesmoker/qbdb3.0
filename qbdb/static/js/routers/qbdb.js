define(['backbone',
        'jquery',
        'underscore',
        'models/tournament',
        'views/tournament',
        'collections/tournaments',
        'views/tournaments',
        'models/packet',
        'views/packet'],
         function(Backbone, $, _, Tournament, TournamentView,
           TournamentCollection, TournamentCollectionView, Packet, PacketView) {

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
              console.log('search');
            },

            read: function() {
              console.log('read');
            },

            showTournament: function(id) {
              console.log('here we load the tournament: ', id)
              var tournament = new Tournament;
              tournament.set('id', id)
              var tournamentView = new TournamentView({model: tournament});
            },

            showPacket: function(id) {
              console.log('here we load the packet: ', id)
              var packet = new Packet;
              packet.set('id', id)
              var packetView = new PacketView({model: packet})
            }

          });

          Backbone.history.start();

          return QBDBRouter;

        });
