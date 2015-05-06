define(
['backbone',
 'jquery',
 'underscore',
 'views/bonus',
 'collections/bonuses'],
 function(Backbone, $, _, BonusView, BonusCollection) {

   var BonusCollectionView = Backbone.View.extend({
     //el: '.bonus-contents',

     initialize: function() {
       this.render();
       this.collection.on('reset', this.render, this);
     },

     render: function() {
       this.$el.html('');
       this.collection.each(function(bonus) {
         this.renderBonus(bonus);
       }, this)

       if (!this.collection.length) {
         $('.bonus-contents').remove()
       }
       return this
     },

     renderBonus: function(bonus) {
       var bonusView = new BonusView({model: bonus});
       bonusEl = bonusView.render().el
       this.$el.append(bonusEl);
     }
   });

   return BonusCollectionView;
});
