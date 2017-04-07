var Backbone = require('backbone');
var _ = require('underscore');
var Packet = require('models/packet');

var PacketCollection = Backbone.Collection.extend({
    model: Packet,

    initialize: function (options) {
        this.tournamentId = options.tournamentId || null;
    },

    getPackets: function(tournamentId) {
        var that = this;
        if (_.isUndefined(tournamentId)) {
            console.log('too many packets')
        } else {
            this.fetch({data: {tournament: tournamentId}, success: function(collection, response) {
                that.set(response['objects']);
            }});
        }
    },

    url: '/api/v1/packet'

});

module.exports = PacketCollection;

