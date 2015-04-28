define(
['backbone',
 'jquery',
 'underscore',
 'views/tossup',
 'collections/tossups'],
 function(Backbone, $, _, TossupView, TossupCollection) {

   var TossupCollectionView = Backbone.View.extend({
     el: '#qbdb-contents',

     initialize: function(collection) {
       this.collection = collection;
       this.render();
       this.collection.on('reset', this.render, this);
     },
 
     render: function() {
       console.log('rendering tossup collection')
       console.log(this.$el)
       this.$el.html('');
       console.log('foobarbaz')
       this.collection.each(function(tossup) {
         console.log('collection: ', this.collection)
         this.renderTossup(tossup);
       }, this);
     },

     renderTossup: function(tossup) {
       console.log('tossup: ', tossup)
       var tossupView = new TossupView({model: tossup});

       this.$el.append(tossupView.render().el);
     }
   });

   return TossupCollectionView;
});
