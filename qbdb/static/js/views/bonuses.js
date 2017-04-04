var Backbone = require('backbone');
//var $ = window.$; // require('jquery');
//var $ui = require('jqueryui');
var _ = require('underscore');
var BonusView = require('views/bonus');

var BonusCollectionView = Backbone.View.extend({
    //el: '.bonus-contents',

    initialize: function () {
        this.render();
        this.collection.on('reset', this.render, this);
    },

    render: function () {
        this.$el.html('');
        this.collection.each(function (bonus) {
            this.renderBonus(bonus);
        }, this);

        if (!this.collection.length) {
            $('.bonus-contents').remove()
        }
        return this
    },

    renderBonus: function (bonus) {
        var bonusView = new BonusView({model: bonus});
        bonusEl = bonusView.render().el
        this.$el.append(bonusEl);
    }
});

module.exports = BonusCollectionView;

