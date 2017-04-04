var Backbone = require('backbone');
//var $ = require('jquery');
var _ = require('underscore');

var Packet = Backbone.Model.extend({
    initialize: function () {

    },

    defaults: {},

    urlRoot: '/api/v1/packet'

});

module.exports = Packet;
