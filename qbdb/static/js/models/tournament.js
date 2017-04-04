var Backbone = require('backbone');
//var $ = require('jquery');
var _ = require('underscore');

var Tournament = Backbone.Model.extend({
    initialize: function () {

    },

    defaults: {},

    urlRoot: '/api/v1/tournament'

});

module.exports = Tournament;

