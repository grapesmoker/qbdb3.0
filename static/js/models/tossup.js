define(['backbone', 'jquery', 'underscore'],
  function(Backbone, $, _) {
    var Tossup = Backbone.Model.extend({
      initialize: function() {
        // this.tossup_text = ''
        // this.answer = ''
      },
      defaults: {
        'tossup_text': '2. This author created a character who tiptoes away immediately after a cat knocks over a cream jar, and screams "Put head back! Put head back!" after a man decapitates a duck with a tomahawk. A story by this author ends with the two main characters constantly interrupting each other until both of them forget what they were going to say, soon after realizing that there\'s no need to stop the organ-grinder. The protagonists of that story by this author, who contemplate dismissing the maid Kate and giving a porter a top-hat, call each other Con and Jug. Jose performs a rousing rendition of "This life is weary" on the piano in this author\'s most famous story, whose protagonist is unable to (*) finish the sentence "Isn\'t life --" after she sees her neighbor\'s corpse. The poor Scott family is brought a basket of leftovers from the title event hosted by the Sheridans in that story by her. For 10 points, name this author of "Prelude," "The Daughters of the Late Colonel," and "The Garden Party," who grew up in New Zealand.',
        'answer': 'Katherine Mansfield'
      }
    });

    return Tossup;
  }
);
