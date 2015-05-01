define(
['backbone',
 'jquery',
 'underscore',
 'views/tournament',
 'collections/tournaments',
 'text!templates/tournaments.html'],
 function(Backbone, $, _, TournamentView, TournamentCollection, TournamentsTemplate) {

   var TournamentCollectionView = Backbone.View.extend({
     el: '#qbdb-contents',


     initialize: function(collection) {
       _.bindAll(this, 'render', 'renderTournament')
       this.collection = collection;
       console.log(this.collection)
       this.render();
       this.collection.on('reset', this.render, this);
     },

     render: function() {
       console.log(this.collection)
       var that = this;
       this.collection.fetch({
         success: function() {
           that.$el.html('');
           that.template = _.template(TournamentsTemplate)
           that.$el.html(that.template({tournaments: that.collection.toJSON()}))
         }
       })

     },

     renderTournament: function(tournament) {
       var tournamentView = new TournamentView({model: tournament});
       console.log(this.$el)
       this.$el.append(tournamentView.render().el);
     }
   });

   return TournamentCollectionView;
});
