var Backbone = require('backbone');
//var $ = require('jquery');
var _ = require('underscore');

var Bonus = Backbone.Model.extend({
    initialize: function () {

    },
    defaults: {},

    getTournamentId: function() {
        var id_pattern = /\/[\d]+\//;
        var tour_id = id_pattern.exec(this.tournament)[0];
        return tour_id.substring(1, tour_id.length - 1);
    }
});

module.exports = Bonus;