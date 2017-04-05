var Backbone = require('backbone');
//var $ = require('jquery');
//var $ui = require('jqueryui');
var _ = require('underscore');
var jst = require('templates/jst');

var TournamentModel = require('models/tournament');
var TournamentTemplate = jst('tournament');

var TournamentView = Backbone.View.extend({

    el: '#qbdb-contents',

    tagName: 'div',

    url: '/api/v1/tournament',

    events: {
        'change .packet-difficulty': function (ev) {
            this.updateDorQ(ev, 'diff')
        },
        'change .packet-quality': function (ev) {
            this.updateDorQ(ev, 'qual')
        }
    },

    initialize: function () {
        this.render()
    },

    render: function () {
        var that = this;
        this.model.fetch().done(function () {
            that.$el.html('');
            that.template = TournamentTemplate;
            that.$el.html(that.template(that.model.attributes));
            return that;
        });
    },

    updateDorQ: function (ev, field) {
        var data = {}
        var packet_id = $(ev.currentTarget).data('packet-id')
        var field_value = $(ev.currentTarget).val()

        data['packet_id'] = packet_id
        data[field] = field_value
        //console.log(field, field_value, packet_id)

        $.post('/vote/', data, function (response) {
            //console.log(response)
            if (response.hasOwnProperty('result') && response.result == 'success') {
                var id = response.id
                var diff = response.diff
                var qual = response.qual
                if (diff > 0) {
                    $('#packet-' + id + '-diff').html(diff)
                }
                else {
                    $('#packet-' + id + '-diff').html('No ratings')
                }
                if (qual > 0) {
                    $('#packet-' + id + '-qual').html(qual)
                }
                else {
                    $('#packet-' + id + '-qual').html('No ratings')
                }
            }
        })
    }
});

module.exports = TournamentView;
