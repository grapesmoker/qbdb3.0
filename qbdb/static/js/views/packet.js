define(['backbone',
        'jquery',
        'underscore',
        'models/packet',
        'collections/tossups',
        'views/tossups',
        'collections/bonuses',
        'views/bonuses',
        'text!templates/packet.html'],
function(Backbone, $, _, PacketModel, TossupCollection, TossupsView,
  BonusCollection, BonusesView, PacketTemplate) {

  var PacketView = Backbone.View.extend({

    el: '#qbdb-contents',

    tagName: 'div',

    initialize: function() {
      this.render()
    },

    events: {

    },

    render: function() {
      var that = this
      //console.log(this.model.id)
      this.model.fetch({success: function() {
        //console.log('foobar')
        that.$el.html('')
        //console.log(that.model.toJSON())
        that.template = _.template(PacketTemplate)
        that.$el.html(that.template())

        var tossups = new TossupCollection(that.model.toJSON().tossups)
        var tossupsView = new TossupsView({collection: tossups, el: $('.tossup-table > tbody')})
        tossupsView.render()

        var bonuses = new BonusCollection(that.model.toJSON().bonuses)
        var bonusesView = new BonusesView({collection: bonuses, el: $('.bonus-table > tbody')})
        bonusesView.render()

        return that;
      },
      error: function() {
        console.log('something bad happened')
      }});
    }
  });

  return PacketView;
});
