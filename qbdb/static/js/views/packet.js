var Backbone = require('backbone');
//var $ = require('jquery');
//var $ui = require('jqueryui');
var _ = require('underscore');
var jst = require('templates/jst');

var PacketModel = require('models/packet');
var TossupCollection = require('collections/tossups');
var TossupsView = require('views/tossups');
var BonusCollection = require('collections/bonuses');
var BonusesView = require('views/bonuses');
var PacketTemplate = jst('packet');

var PacketView = Backbone.View.extend({

    el: '#qbdb-contents',

    tagName: 'div',

    initialize: function () {
        this.render()
    },

    events: {},

    render: function () {
        var that = this;
        //console.log(this.model.id)
        this.model.fetch({
            success: function () {
                //console.log('foobar')
                that.$el.html('');
                console.log(that.model.toJSON())
                that.template = PacketTemplate;
                that.$el.html(that.template());

                console.log('author: ', that.model.get('author'))
                var tossups = new TossupCollection(that.model.get('tossups'));
                var tossupsView = new TossupsView({collection: tossups, el: $('.tossup-table > tbody'),
                    author: that.model.get('author')});
                tossupsView.render();

                var bonuses = new BonusCollection(that.model.toJSON().bonuses);
                var bonusesView = new BonusesView({collection: bonuses, el: $('.bonus-table > tbody')});
                bonusesView.render();

                return that;
            },
            error: function () {
                console.log('something bad happened')
            }
        });
    }
});

module.exports = PacketView;

