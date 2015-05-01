define(['backbone',
        'jquery',
        'underscore',
        'models/tossup',
        'text!templates/tossup.html',
        'text!templates/tossup_as_row.html'],
function(Backbone, $, _, TossupModel, tossupTemplate, tuAsRowTemplate) {

  var TossupView = Backbone.View.extend({

    tagName: 'tr',

    initialize: function() {
      //this.render()
      /*if !(_.isUndefined(options.viewType)) {
        this.viewType = options.viewType
        console.log('view type: ', this.viewType)
      }*/
    },

    events: {

    },

    render: function() {
      this.template = _.template(tuAsRowTemplate)
      this.$el.html(this.template(this.model.toJSON()));

      return this;
    }
  });

  return TossupView
});
