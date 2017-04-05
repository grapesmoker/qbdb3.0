var Backbone = require('backbone');
//var $ = require('jquery');
//var $ui = require('jqueryui');
var _ = require('underscore');
var jst = require('templates/jst');

var TossupModel = require('models/tossup');
var TossupTemplate = jst('tossup');
var TuAsRowTemplate = jst('tossup_as_row');

var TossupView = Backbone.View.extend({

    tagName: 'tr',

    initialize: function () {

    },

    events: {
        'change .tossup-difficulty': function (ev) {
            this.updateDorQ(ev, 'diff')
        },
        'change .tossup-quality': function (ev) {
            this.updateDorQ(ev, 'qual')
        }
    },

    render: function () {
        this.template = TuAsRowTemplate;
        this.$el.html(this.template(this.model.attributes));

        return this;
    },

    updateDorQ: function (ev, field) {
        var data = {};
        var tour_id = $(ev.currentTarget).data('tossup-id');
        var field_value = $(ev.currentTarget).val();

        data['tossup_id'] = tour_id;
        data[field] = field_value;
        //console.log(field, field_value, tour_id)

        $.post('/vote/', data, function (response) {
            //console.log(response)
            if (response.hasOwnProperty('result') && response.result == 'success') {
                var id = response.id;
                var diff = response.diff;
                var qual = response.qual;
                if (diff > 0) {
                    $('#tossup-' + id + '-diff').html(diff)
                }
                else {
                    $('#tossup-' + id + '-diff').html('No ratings')
                }
                if (qual > 0) {
                    $('#tossup-' + id + '-qual').html(qual)
                }
                else {
                    $('#tossup-' + id + '-qual').html('No ratings')
                }
            }
        })
    }

});

module.exports = TossupView;

