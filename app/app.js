// Declare app level module which depends on views, and components
'use strict'
angular.module('PokerMain', [

    ])


.controller('PokerCtrl', function($scope, $http){
        $scope.version = 0.6;

        $http.get("http://www.w3schools.com/angular/customers.php")
                .success(function(response) {
                    $scope.names = response.records;
            });

        //number of players
        $scope.players_nr = 6;

        //card prototype
        $scope.card = {
            face: 'A',
            suit: 'Spades'
        };

        //server settings
        $scope.host = 'localhost';
        $scope.size = 1024;
        $scope.port = 10000;


        //image location
        $scope.getImageLocation = function(face, suit){
          return 'url(components/images/cards/' + face + '_of_' + suit + '.png)';
        };

        //maximum amount in players' contributions
        Array.max = function( array ){
            return Math.max.apply( Math, array );
        };

        $scope.getMax = function(){
            return Array.max( $scope.player_contribution );
        };

        //------------------- cards on the center: flop, river, turn ---
        //values
        $scope.flop = [
            {face: 'A', suit: 'Clubs'},
            {face: 'A', suit: 'Spades'},
            {face: 'A', suit: 'Spades'}
            ];
        $scope.flop.is_visible = true;

        $scope.turn = {
            face: 'A', suit: 'Hearts',
            is_visible: true
        };
        $scope.river = {
            face: 'A', suit: 'Clubs',
            is_visible: true
        };


        //------------------- players ----------------------------------
        $scope.is_player_visible = [
            true, true, true, true, true, true
        ];
        $scope.is_dealer = [
            true, true, true, true, true, true
        ];
        $scope.is_small_blind = [
            true, true, true, true, true, true
        ];
        $scope.is_big_blind = [
            true, true, true, true, true, true
        ];
        $scope.is_card_visible = [
            true, false, false, false, false, false
        ];

        $scope.dealer = 1;
        $scope.big_blind = ($scope.dealer + 2) % ($scope.players_nr);
        $scope.small_blind = ($scope.dealer + 1) % ($scope.players_nr);

        $scope.game_has_started = true;

        $scope.player_name = [
            'popek', 'tomasz', 'maciej', 'popek', 'tomasz', 'maciej'
        ];

        $scope.player_cards = [
            {first_card: {face: 'A', suit: 'Spades'},  second_card: {face: 'A', suit: 'Hearts'}},
            {first_card: {face: 'A', suit: 'Spades'},  second_card: {face: 'A', suit: 'Hearts'}},
            {first_card: {face: 'A', suit: 'Spades'},  second_card: {face: 'A', suit: 'Hearts'}},
            {first_card: {face: 'A', suit: 'Spades'},  second_card: {face: 'A', suit: 'Hearts'}},
            {first_card: {face: 'A', suit: 'Spades'},  second_card: {face: 'A', suit: 'Hearts'}},
            {first_card: {face: 'A', suit: 'Spades'},  second_card: {face: 'A', suit: 'Hearts'}}
        ];

        $scope.player_remaining_time = [

        ];

        $scope.player_contribution = [
            1,12,3,4,5,6
        ];

        $scope.player_stack = [
            1,2,3,4,5,6
        ];

        $scope.player_turn = {

        };

        $scope.is_player_ready = [

        ];

        $scope.new_bet = '';

        $scope.setStand = function(number) {
            $scope.is_player_visible[number - 1] = false;
        };
        $scope.setFold = function() {
            $scope.fold.status = true;
        };
        $scope.setCall = function() {
            $scope.call.status = true;
        };
        $scope.setReady = function() {
            $scope.ready.status = true;
        };
        $scope.setRaise = function() {
            $scope.raise.status = true;
        };

        $scope.getBetAmount = function(){
            return $scope.bet.amount;
        };

        $scope.setBet = function(val) {
            if (val !== '' && val !== undefined) {
                $scope.bet.amount = val;
                val = 0;
            }
        };


        //------------------- buttons ---------------------------------
        $scope.sit = {
            button_disabled: false,
            status: false
        };
        $scope.stand = {
            button_disabled: false,
            status: false
            };
        $scope.call = {
            button_disabled: true,
            status: false
        };
        $scope.raise = {
            button_disabled: true,
            status: false
        };
        $scope.ready = {
            button_disabled: false,
            status: false
        };
        $scope.fold = {
            button_disabled: true,
            status: false
        };
        $scope.bet = {
            button_disabled: false,
            status: false,
            amount: 0
        };

        //checks if any button should be disabled
        $scope.checkButtons = function() {
        };

        //--------------------chat and game history--------------------
        $scope.chat_entries = [];
        $scope.entry = '';
        $scope.is_logged = false;

        $scope.user_login = 'popek';
        $scope.new_user_login = '';
        $scope.new_entry = '';

        $scope.setLogin = function (){
            if($scope.new_user_login !== '') {
                $scope.user_login = $scope.new_user_login;
                $scope.new_user_login = '';
                $scope.is_logged = true;
            }
        };

        $scope.addChatEntry = function (){
            console.log($scope.new_entry);
            if($scope.new_entry !== ''  && $scope.new_entry !== undefined) {
                $scope.chat_entries.push({
                    string: $scope.new_entry,
                    author: $scope.user_login,
                    dt: new Date()
                });
                $scope.new_entry = '';
            }
        };

        $scope.decode_utf8 =  function (s) {
            return unescape(encodeURIComponent(s));
        }

    })
;
