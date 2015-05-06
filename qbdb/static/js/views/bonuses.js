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
       //this.collection = collection;
       this.render();
       this.collection.on('reset', this.render, this);
       /*if (_.isUndefined(options.viewType)) {
         this.viewType = options.viewType
       } else { this.viewType  = 'asDiv'}*/
     },

     render: function() {
       this.$el.html('');
       //console.log(this.$el)
       //console.log(this.collection)
       this.collection.each(function(bonus) {
         this.renderBonus(bonus);
       }, this);
     },

     renderBonus: function(bonus) {
       var bonusView = new BonusView({model: bonus});
       bonusEl = bonusView.render().el
       this.$el.append(bonusEl);
     }
   });

   return BonusCollectionView;
});
