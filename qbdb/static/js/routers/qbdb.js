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
var FAQ = jst('faq');

var ReaderView = require('views/reader');

var QBDBRouter = Backbone.Router.extend({
    routes: {
        'browse': 'browse',
        'search': 'search',
        'read': 'read',
        'tournament/:id': 'showTournament',
        'packet/:id': 'showPacket',
        'faq': 'faq'
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
    },

    read: function () {
        var reader = new ReaderView({});
    },

    showTournament: function (id) {
        var tournament = new Tournament;
        tournament.set('id', id);
        var tournamentView = new TournamentView({model: tournament});
    },

    showPacket: function (id) {
        var packet = new Packet;
        packet.set('id', id);
        var packetView = new PacketView({model: packet})
    },

    faq: function() {
        console.log('faq');
        console.log(FAQ());

        $('#qbdb-contents').html(FAQ());
    }

});

Backbone.history.start();

module.exports = QBDBRouter;

