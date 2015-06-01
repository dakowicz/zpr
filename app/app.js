// Declare app level module which depends on views, and components
'use strict'
angular.module('PokerMain', [

])

.controller('PokerMainCtrl', function($scope){
        $scope.version = 0.5;
        $scope.card_types = [
        ];

        //game variables
        $scope.big_blind = 2;
        $scope.small_blind = 1;

        //card prototype
        $scope.card = {
            face: 'ace',
            suit: 'spades'
        };

        //image location
        $scope.getImageLocation = function(face, suit){
          return 'url(components/images/cards/' + face + '_of_' + suit + '.png)';
        };

        //------------------- cards on the center: flop, river, turn ---
        //values
        $scope.flop = [
            {face: 'ace', suit: 'spades'},
            {face: 'ace', suit: 'spades'},
            {face: 'ace', suit: 'spades'}
            ];
        $scope.flop.is_visible = true;

        $scope.turn = {
            face: 'ace', suit: 'hearts',
            is_visible: true
        };
        $scope.river = {
            face: 'ace', suit: 'clubs',
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

        $scope.player_name = [

        ];

        $scope.player_cards = [
            {first_card: {face: 'ace', suit: 'spades'},  second_card: {face: 'ace', suit: 'hearts'}},
            {first_card: {face: 'ace', suit: 'spades'},  second_card: {face: 'ace', suit: 'hearts'}},
            {first_card: {face: 'ace', suit: 'spades'},  second_card: {face: 'ace', suit: 'hearts'}},
            {first_card: {face: 'ace', suit: 'spades'},  second_card: {face: 'ace', suit: 'hearts'}},
            {first_card: {face: 'ace', suit: 'spades'},  second_card: {face: 'ace', suit: 'hearts'}},
            {first_card: {face: 'ace', suit: 'spades'},  second_card: {face: 'ace', suit: 'hearts'}}
        ];

        $scope.player_remaining_time = [

        ];

        $scope.player_bet = [

        ];

        $scope.player_stack = [
            1,2,3,4,5,6
        ];

        $scope.setSit = function(number) {
            $scope.is_player_visible[number - 1] = true;
        };
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


        //--------------------chat and game history--------------------
        $scope.chat_entries = [];
        $scope.entry = '';

        $scope.login = 'popek';

        $scope.addChatEntry = function (){
            if($scope.entry !== '') {
                $scope.chat_entries.push({
                    entry_string: $scope.entry,
                    author: $scope.login
                });

            }
        };

    })
;
