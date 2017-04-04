var Backbone = require('backbone');
//var $ = require('jquery');
//var $ui = require('jqueryui');
var _ = require('underscore');

var TossupView = require('views/tossup');

var TossupCollectionView = Backbone.View.extend({
    //el: '.tossup-contents',

    initialize: function (options) {
        this.render();
        this.collection.on('reset', this.render, this);
        this.author = options.author;
    },

    render: function () {
        this.$el.html('');
        this.collection.each(function (tossup) {
            this.renderTossup(tossup);
        }, this);
        if (!this.collection.length) {
            $('.tossup-contents').remove()
        }
        return this
    },

    renderTossup: function (tossup) {
        var tossupView = new TossupView({model: tossup});
        tossupEl = tossupView.render().el;
        this.$el.append(tossupEl);
    }
});

module.exports = TossupCollectionView;
