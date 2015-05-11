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
      'change .bonus-difficulty': function(ev) { this.updateDorQ(ev, 'diff') },
      'change .bonus-quality': function(ev) { this.updateDorQ(ev, 'qual') }
    },

    render: function() {
      this.template = _.template(bsAsRowTemplate)
      this.$el.html(this.template(this.model.toJSON()));

      return this;
    },

    updateDorQ: function(ev, field) {
      var data = {}
      var tour_id = $(ev.currentTarget).data('bonus-id')
      var field_value = $(ev.currentTarget).val()

      data['bonus_id'] = tour_id
      data[field] = field_value
      //console.log(field, field_value, tour_id)

      $.post('/vote/', data, function(response) {
        //console.log(response)
        if (response.hasOwnProperty('result') && response.result == 'success') {
          var id = response.id
          var diff = response.diff
          var qual = response.qual
          if (diff > 0) {
            $('#bonus-' + id + '-diff').html(diff)
          }
          else {
            $('#bonus-' + id + '-diff').html('No ratings')
          }
          if (qual > 0) {
            $('#bonus-' + id + '-qual').html(qual)
          }
          else {
            $('#bonus-' + id + '-qual').html('No ratings')
          }
        }
      })
    }
  });

  return BonusView
});
