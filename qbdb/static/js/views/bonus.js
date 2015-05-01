define(['backbone',
        'jquery',
        'underscore',
        'models/bonus',
        'text!templates/bonus_as_row.html'],
function(Backbone, $, _, BonusModel, bsAsRowTemplate) {

  var BonusView = Backbone.View.extend({

    tagName: 'tr',

    initialize: function() {

    },

    events: {

    },

    render: function() {
      this.template = _.template(bsAsRowTemplate)
      this.$el.html(this.template(this.model.toJSON()));

      return this;
    }
  });

  return BonusView
});
