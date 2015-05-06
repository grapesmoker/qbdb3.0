define(
['backbone',
 'jquery',
 'underscore',
 'views/tossup',
 'collections/tossups'],
 function(Backbone, $, _, TossupView, TossupCollection) {

   var TossupCollectionView = Backbone.View.extend({
     //el: '.tossup-contents',

     initialize: function() {
       this.render();
       this.collection.on('reset', this.render, this);
     },

     render: function() {
       this.$el.html('');
       this.collection.each(function(tossup) {
         this.renderTossup(tossup);
       }, this)
       if (!this.collection.length) {
         $('.tossup-contents').remove()
       }
       return this
     },

     renderTossup: function(tossup) {
       var tossupView = new TossupView({model: tossup});
       tossupEl = tossupView.render().el
       this.$el.append(tossupEl);
     }
   });

   return TossupCollectionView;
});
