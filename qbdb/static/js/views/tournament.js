define(['backbone',
        'jquery',
        'underscore',
        'models/tournament',
        'text!templates/tournament.html'],
function(Backbone, $, _, TournamentModel, tournamentTemplate) {

  var TournamentView = Backbone.View.extend({

    el: '#qbdb-contents',

    tagName: 'div',

    initialize: function() {
      this.render()
    },

    events: {

    },

    render: function() {
      var that = this
      console.log(this.model.id)
      this.model.fetch().done(function() {
        that.$el.html('')
        console.log(that.model.toJSON())
        that.template = _.template(tournamentTemplate)
        that.$el.html(that.template(that.model.toJSON()));
        return that;
      })
    }
  });

  return TournamentView;
});
