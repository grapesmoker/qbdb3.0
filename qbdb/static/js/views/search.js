var Backbone = require('backbone');
//var $ = require('jquery');
//var $ui = require('jqueryui');
var _ = require('underscore');
var jst = require('templates/jst');

var TossupModel = require('models/tossup');
var BonusModel = require('models/bonus');
var TossupsCollection = require('collections/tossups');
var BonusesCollection = require('collections/bonuses');
var TossupsView = require('views/tossups');
var BonusesView = require('views/bonuses');
var SearchTemplate = jst('search');
var PacketTemplate = jst('packet');


var SearchView = Backbone.View.extend({

    el: '#search-results',

    initialize: function () {

    },

    events: {
        'click #search': 'searchAndRender',
        'keypress #search-term': 'keyHandler',
        'change #search-term': 'logChange'
    },

    render: function () {
        this.template = SearchTemplate;
        this.$el.html(this.template());
        return this;
    },

    keyHandler: function (ev) {
        if (ev.charCode == 13) {
            ev.preventDefault()
            this.searchAndRender();
        }
    },

    logChange: function () {
        //console.log('change')
    },

    searchAndRender: function () {
        var that = this
        var data = this.$el.find('#search-form').serializeArray()
        $.get('/search', data, function (result) {

            console.log(result);

            var result_el = $('#search-results')
            if (result_el.length) {
                result_el.html('')
            } else {
                $('#qbdb-contents').append('<div id="search-results"></div>')
                result_el = $('#qbdb-contents > #search-results')
            }

            var template = PacketTemplate;
            result_el.html(template());

            var tossups = new TossupsCollection(result.tossups)
            var bonuses = new BonusesCollection(result.bonuses)

            var tossupsView = new TossupsView({collection: tossups, el: $('.tossup-table > tbody')})
            tossupsView.render()

            var bonusesView = new BonusesView({collection: bonuses, el: $('.bonus-table > tbody')})
            bonusesView.render()

        })
    }
});

module.exports = SearchView

