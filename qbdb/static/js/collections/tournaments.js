var Backbone = require('backbone');
//var $ = require('jquery');
var _ = require('underscore');

var Tournament = require('models/tournament');


var TournamentCollection = Backbone.Collection.extend({
    model: Tournament,

    initialize: function () {

    },

    url: '/api/v1/tournament'

});

module.exports = TournamentCollection;

