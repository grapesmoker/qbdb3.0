var Backbone = require('backbone');
//var $ = require('jquery');
//var $ui = require('jqueryui');
var _ = require('underscore');
var jst = require('templates/jst');

var TournamentView = require('views/tournament');
var TournamentCollection = require('collections/tournaments');
var TournamentsTemplate = jst('tournaments');

var TournamentCollectionView = Backbone.View.extend({
    el: '#qbdb-contents',

    events: {
        'change .tour-difficulty': function (ev) {
            this.updateDorQ(ev, 'diff')
        },
        'change .tour-quality': function (ev) {
            this.updateDorQ(ev, 'qual')
        }
    },

    initialize: function (collection) {
        _.bindAll(this, 'render', 'renderTournament')
        this.collection = collection;
        this.render();
        this.collection.on('reset', this.render, this);
    },

    render: function () {
        var that = this;
        this.collection.fetch({
            success: function (collection, response, options) {
                that.$el.html('');
                that.collection.set(response['objects']);
                that.template = TournamentsTemplate;
                that.$el.html(that.template({tournaments: that.collection.models}))
            }
        })

    },

    renderTournament: function (tournament) {
        var tournamentView = new TournamentView({model: tournament});
        this.$el.append(tournamentView.render().el);
    },

    updateDorQ: function (ev, field) {
        var data = {}
        var tour_id = $(ev.currentTarget).data('tournament-id')
        var field_value = $(ev.currentTarget).val()

        data['tournament_id'] = tour_id
        data[field] = field_value
        //console.log(field, field_value, tour_id)

        $.post('/vote/', data, function (response) {
            //console.log(response)
            if (response.hasOwnProperty('result') && response.result == 'success') {
                var id = response.id
                var diff = response.diff
                var qual = response.qual
                if (diff > 0) {
                    $('#tournament-' + id + '-diff').html(diff)
                }
                else {
                    $('#tournament-' + id + '-diff').html('No ratings')
                }
                if (qual > 0) {
                    $('#tournament-' + id + '-qual').html(qual)
                }
                else {
                    $('#tournament-' + id + '-qual').html('No ratings')
                }
            }
        })
    }
});

module.exports = TournamentCollectionView;

