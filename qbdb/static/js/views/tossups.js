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
       //this.collection = collection;
       this.render();
       this.collection.on('reset', this.render, this);
       /*if (_.isUndefined(options.viewType)) {
         this.viewType = options.viewType
       } else { this.viewType  = 'asDiv'}*/
     },

     render: function() {
       this.$el.html('');
       console.log(this.$el)
       console.log(this.collection)
       this.collection.each(function(tossup) {
         this.renderTossup(tossup);
       }, this);
     },

     renderTossup: function(tossup) {
       var tossupView = new TossupView({model: tossup});
       tossupEl = tossupView.render().el
       this.$el.append(tossupEl);
     }
   });

   return TossupCollectionView;
});
