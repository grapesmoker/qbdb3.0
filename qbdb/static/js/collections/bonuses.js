var Backbone = require('backbone');
//var $ = require('jquery');
var _ = require('underscore');
var Bonus = require('models/bonus');
var BonusView = require('views/bonus');

var BonusCollection = Backbone.Collection.extend({
    model: Bonus,

    initialize: function () {
        console.log('init bonus collection')
    }

});

module.exports = BonusCollection;

