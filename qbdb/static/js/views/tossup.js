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

    },

    events: {
      'change .tossup-difficulty': function(ev) { this.updateDorQ(ev, 'diff') },
      'change .tossup-quality': function(ev) { this.updateDorQ(ev, 'qual') }
    },

    render: function() {
      this.template = _.template(tuAsRowTemplate)
      this.$el.html(this.template(this.model.toJSON()));

      return this;
    },

    updateDorQ: function(ev, field) {
      var data = {}
      var tour_id = $(ev.currentTarget).data('tossup-id')
      var field_value = $(ev.currentTarget).val()

      data['tossup_id'] = tour_id
      data[field] = field_value
      //console.log(field, field_value, tour_id)

      $.post('/vote/', data, function(response) {
        //console.log(response)
        if (response.hasOwnProperty('result') && response.result == 'success') {
          var id = response.id
          var diff = response.diff
          var qual = response.qual
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

  return TossupView
});
