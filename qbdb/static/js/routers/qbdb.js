var Backbone = require('backbone');
//var $ = require('jquery');
//var $ui = require('jqueryui');
var _ = require('underscore');
var jst = require('templates/jst');

var bs = require('bootstrap');

var Tournament = require('models/tournament');
var TournamentView = require('views/tournament');
var TournamentCollection = require('collections/tournaments');
var TournamentCollectionView = require('views/tournaments');

var Packet = require('models/packet');
var PacketView = require('views/packet');

var SearchView = require('views/search');
var Dialog = jst('dialog');


var QBDBRouter = Backbone.Router.extend({
    routes: {
        'browse': 'browse',
        'search': 'search',
        'read': 'read',
        'tournament/:id': 'showTournament',
        'packet/:id': 'showPacket'
    },

    browse: function () {
        var tournaments = new TournamentCollection();
        var tourView = new TournamentCollectionView(tournaments);
    },

    search: function () {
        var el = $('#qbdb-contents');
        el.html('');
        var searchView = new SearchView({el: el});
        searchView.render();
        // el.html(searchView.render().el)
    },

    read: function () {
        var el = $('#qbdb-contents');
        el.html('<div class="col-md-offset-2 col-md-8">' +
            '<p class="bg-warning">' + 'This feature is not available yet.' + '</p></div>');

        var dialog = Dialog({
            text: 'This feature is not available yet.',
            title: 'Unimplemented feature.'
        });
        
        $(dialog).modal('show');
    },

    showTournament: function (id) {
        console.log('show tournament');
        var tournament = new Tournament;
        tournament.set('id', id);
        var tournamentView = new TournamentView({model: tournament});
    },

    showPacket: function (id) {
        console.log('show packet');
        var packet = new Packet;
        packet.set('id', id);
        var packetView = new PacketView({model: packet})
    },

    showTossup: function (id) {

    }

});

Backbone.history.start();

module.exports = QBDBRouter;

