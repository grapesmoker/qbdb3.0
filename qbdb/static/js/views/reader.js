var Backbone = require('backbone');
var _ = require('underscore');
var jst = require('templates/jst');
var ReaderTemplate = jst('reader');

var TossupModel = require('models/tossup');
var TossupCollection = require('collections/tossups');
var BonusModel = require('models/bonus');
var BonusCollection = require('collections/bonuses');
var PacketModel = require('models/packet');
var TournamentCollection = require('collections/tournaments');

var ReaderView = Backbone.View.extend({

    el: '#qbdb-contents',

        initialize: function(options) {
        this.speed = options.speed || 3;
        this.order = options.order || 'sequential';
        this.readTossups = options.readTossups || true;
        this.readBonuses = options.readBonuses || true;

        this.currentQuestion = null;
        this.currentQType = null;
        this.currentPacket = null;
        this.currentTournament = null;
        this.questionsToRead = [];
        this.questionBeingRead = false;
        this.bonusPartBeingRead = 0;
        this.readTimer = null;

        this.render()
    },

    events: {
        'click #start-reading': 'startReading',
        'click #next-question': 'nextQuestion',
        'click #next-bonus-part': 'nextBonusPart',
        'click #show-answer': 'showAnswer',
        'click #buzz': 'buzz',
        'input #read-tournament': 'populatePackets',
        'input #read-packet': 'setCurrentPacket',
        'click #read-tossups': 'changeOptions',
        'click #read-bonuses': 'changeOptions',
        'click #read-order': 'changeOptions',
        'input #read-speed': 'changeOptions'
    },

    render: function() {
        var reader_template = ReaderTemplate();
        this.$el.html(reader_template);
        this.populateTournaments()
    },

    populateTournaments: function() {
        var tournaments = new TournamentCollection();
        this.tournaments = tournaments;
        tournaments.fetch({success: function(collection, response) {
            tournaments.set(response['objects']);
            _.each(collection.models, function(tournament) {
                var option = '<option value="' + tournament.get('id') + '">' +
                    tournament.get('tournament_name') + '</option>';
                $('#read-tournament').append(option);
            });
        }});
    },

    populatePackets: function() {
        var tournament_id = $('#read-tournament').val();
        if (tournament_id != 0) {
            var tournament = this.tournaments.get(tournament_id);
            this.currentTournament = tournament;
            $('#read-packet').html('<option value="0">Any (random)</option>');
                _.each(tournament.get('packets'), function(packet) {
                var option = '<option value="' + packet.id + '">' + packet.author + '</option>';
                $('#read-packet').append(option);
            });
        } else {
            this.currentTournament = null
        }
    },

    setCurrentPacket: function() {
        var that = this;
        var packet_id = $('#read-packet').val();
        if (packet_id != 0) {
            var packet = new PacketModel({id: packet_id});
            packet.fetch({success: function(model, response) {
                that.currentPacket = model;
            }})
        } else {
            that.currentPacket = null;
        }
    },

    startReading: function() {
        var that = this;
        var questions = [], tossups = [], bonuses = [];
        if (this.currentTournament && this.currentPacket) {

            if (this.readTossups) {
                tossups = this.currentPacket.get('tossups');
            }
            if (this.readBonuses) {
                bonuses = this.currentPacket.get('bonuses');
            }
            questions = tossups.concat(bonuses);
            if (this.order == 'random') {
                this.questionsToRead = _.shuffle(questions);
            } else {
                this.questionsToRead = questions.reverse();
            }
            that.nextQuestion();
        } else if (this.currentTournament) {
            var tossupsPromise = new Promise(function(resolve, reject) {
                if (!that.readTossups) {
                    resolve(false)
                } else {
                    var tossups = new TossupCollection();
                    tossups.fetch({data: {tournament: that.currentTournament.get('id')},
                        success: function(collection, response) {
                            collection.set(response['objects']);
                            resolve(collection);
                    }});
                }
            }, []);
            var bonusesPromise = new Promise(function(resolve, reject) {
                if (!that.readBonuses) {
                    resolve(false);
                } else {
                    var bonuses = new BonusCollection();
                    bonuses.fetch({data: {tournament: that.currentTournament.get('id')},
                        success: function(collection, response) {
                            collection.set(response['objects']);
                            resolve(collection);
                    }});
                }

            }, []);

            Promise.all([tossupsPromise, bonusesPromise]).then(function(collections) {
                if (collections[0]) {
                    tossups = _.map(collections[0].models, function(tossup) {
                        return tossup.attributes;
                    });
                }
                if (collections[1]) {
                    bonuses = _.map(collections[1].models, function(bonus) {
                        return bonus.attributes;
                    });
                }
                questions = tossups.concat(bonuses);
                if (that.order == 'random') {
                    that.questionsToRead = _.shuffle(questions);
                } else {
                    that.questionsToRead = questions.reverse()
                }
                that.nextQuestion()
            })
        } else {
            that.nextQuestion();
        }
        // countdown
    },

    readQuestion: function() {
        var that = this;
        var header = $('#reader-question-header');
        var question_type = null;
        var question_text = $('#reader-question-text');

        if (_.has(that.currentQuestion, 'tossup_text')) {
            question_type = 'tossup';
            question_text.html('');
            var interval = 1000.0 - 150.0 * this.speed;
            console.log(interval);
            var words = that.currentQuestion.tossup_text.split(' ').reverse();
            that.questionBeingRead = true;
            that.readTimer = setInterval(function() {
                if (that.questionBeingRead) {
                    var currentText = question_text.html();
                    currentText += ' ' + words.pop();
                    question_text.html(currentText);
                    if (words.length == 0) {
                        clearInterval(that.readTimer);
                    }
                }
            }, interval)
        } else if (_.has(that.currentQuestion, 'bonus_parts')) {
            question_type = 'bonus';
            if (this.bonusPartBeingRead == 0) {
                question_text.html('<p>' + this.currentQuestion.leadin + '</p><p>' +
                    this.currentQuestion.bonus_parts[0].text + '</p>');
            } else {
                question_text.html(question_text.html() +
                    '<p>' + this.currentQuestion.bonus_parts[this.bonusPartBeingRead].text + '</p>')
            }
        }

        header.html('<h4>Reading ' + question_type + ' ' + that.currentQuestion.number +
            ' in packet ' + that.currentQuestion.author +
            ' in tournament ' + that.currentQuestion.tournament_name + '</h4>');
    },

    buzz: function() {
        if (this.questionBeingRead) {
            this.questionBeingRead = false;
            $('#buzz').text('Continue');
        } else {
            this.questionBeingRead = true;
            $('#buzz').text('Buzz');
        }
    },

    nextQuestion: function() {
        var that = this;

        if (!this.currentTournament && !this.currentPacket) {
            var question_type = null;
            if (this.readTossups && this.readBonuses) {
                question_type = 'either'
            } else if (this.readTossups) {
                question_type = 'tossup'
            } else if (this.readBonuses) {
                question_type = 'bonus'
            }
            $.get('/random', {question_type: question_type}, function(result) {
                that.currentQuestion = result;
                that.bonusPartBeingRead = 0;
                clearInterval(that.readTimer);
                $('#buzz').text('Buzz');
                $('#reader-answer').html('');
                $('#reader-question-footer').html('');
                that.readQuestion();
            })
        } else if (this.questionsToRead.length >= 1) {
            this.currentQuestion = this.questionsToRead.pop();
            this.bonusPartBeingRead = 0;
            clearInterval(this.readTimer);
            $('#buzz').text('Buzz');
            $('#reader-answer').html('');
            $('#reader-question-footer').html('');
            this.readQuestion();
        } else {
            var alert = '<div class="alert alert-warning">There are no more questions to read!</div>';
            $('#reader-question-footer').html(alert);
        }
    },

    nextBonusPart: function() {
        if (_.has(this.currentQuestion, 'bonus_parts')) {
            if (this.bonusPartBeingRead < this.currentQuestion.bonus_parts.length - 1) {
                this.bonusPartBeingRead += 1
                $('#reader-question-footer').html('')
                this.readQuestion();
            } else {
                var alert = '<div class="alert alert-warning">There are no more bonus parts to read!</div>';
                $('#reader-question-footer').html(alert);
            }
        } else {
            var alert = '<div class="alert alert-warning">This isn\'t a bonus!</div>';
            $('#reader-question-footer').html(alert);
        }
    },

    showAnswer: function() {
        if (_.has(this.currentQuestion, 'tossup_text')) {
            $('#reader-answer').html(this.currentQuestion.answer);
        } else if (_.has(this.currentQuestion, 'bonus_parts')) {
            var answer_text = this.currentQuestion.bonus_parts[this.bonusPartBeingRead].answer;
            $('#reader-answer').html(answer_text);
        }
    },

    stopReading: function() {
        console.log('stop reading')
    },

    changeOptions: function() {
        this.readTossups = $('#read-tossups').is(':checked');
        this.readBonuses = $('#read-bonuses').is(':checked');
        this.speed = $('#read-speed').val();
        this.order = $('#read-order:checked').val();
        if (this.order == 'random') {
            this.questionsToRead = _.shuffle(this.questionsToRead);
        }
    }
});

module.exports = ReaderView;