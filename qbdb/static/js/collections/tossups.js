var Backbone = require('backbone');
//var $ = require('jquery');
var _ = require('underscore');

var TossupModel = require('models/tossup');

var TossupCollection = Backbone.Collection.extend({
    model: TossupModel,

    initialize: function (options) {
        console.log('init tossup collection')
    }


});

module.exports = TossupCollection;

