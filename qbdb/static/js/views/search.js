define(['backbone',
        'jquery',
        'underscore',
        'models/tossup',
        'models/bonus',
        'collections/tossups',
        'collections/bonuses',
        'views/tossups',
        'views/bonuses',
        'text!templates/search.html',
        'text!templates/packet.html'],
function(Backbone, $, _, TossupModel, BonusModel,
  TossupsCollection, BonusesCollection,
  TossupsView, BonusesView, searchTemplate, packetTemplate) {

  var SearchView = Backbone.View.extend({

    el: '#search-results',

    initialize: function() {

    },

    events: {
      'click #search': 'searchAndRender',
    },

    render: function() {
      this.template = _.template(searchTemplate)
      this.$el.html(this.template())
      return this;
    },

    searchAndRender: function() {
      var that = this
      var data = this.$el.find('#search-form').serializeArray()
      $.get('/search', data, function(result) {
        console.log(result)

        var result_el = $('#search-results')
        if (result_el.length) {
          result_el.html('')
        } else {
          $('#qbdb-contents').append('<div id="search-results"></div>')
          result_el = $('#qbdb-contents > #search-results')
        }

        var template = _.template(packetTemplate)
        result_el.html(template())

        var tossups = new TossupsCollection(result.tossups)
        var bonuses = new BonusesCollection(result.bonuses)

        var tossupsView = new TossupsView({collection: tossups, el: $('.tossup-table > tbody')})
        tossupsView.render()

        var bonusesView = new BonusesView({collection: bonuses, el: $('.bonus-table > tbody')})
        bonusesView.render()

      })
    }
  });

  return SearchView
});
