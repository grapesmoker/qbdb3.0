var Backbone = require('backbone');
//var $ = require('jquery');
var _ = require('underscore');
var Bonus = require('models/bonus');
var BonusView = require('views/bonus');

var BonusCollection = Backbone.Collection.extend({
    model: Bonus,

    initialize: function () {

    },

    url: '/api/v1/bonus'

});

module.exports = BonusCollection;

