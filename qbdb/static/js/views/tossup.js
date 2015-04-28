define(['backbone',
        'jquery',
        'underscore',
        'models/tossup',
        'text!templates/tossup.html'],
function(Backbone, $, _, TossupModel, tossupTemplate) {

  var TossupView = Backbone.View.extend({

    tagName: 'div',

    initialize: function() {
      console.log('init TossupView')
      this.render()
    },

    events: {

    },

    render: function() {
      console.log('render TossupView')

      console.log(this.model.tossup_text)
      console.log(this.model.answer)

      this.template = _.template(tossupTemplate,
        {tossup_text: this.model.tossup_text,
         answer: this.model.answer});

      console.log(this.template)
      console.log(this.el)

      this.$el.html(this.template);

      return this;
    }
  });

  return TossupView
});
