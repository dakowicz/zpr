
//'use strict';

//var socket = new WebSocket("ws://localhost:10000/");

angular.module('PokerMain', [])
    .controller('PokerCtrl', function($scope) {

        //setting up a connection
        $scope.socket =  new WebSocket("ws://localhost:10000/");

        //$scope.socket = undefined
        //$scope.socket == undefined ? $scope.socket = new WebSocket("ws://localhost:10000/") : console.log("attempt to create connection");

        //setting up property watchers

        //command texts
        $scope.READY_COMMAND = 'start';
        $scope.CALL_COMMAND = 'call';
        $scope.BET_COMMAND = 'bet';
        $scope.RAISE_COMMAND = 'raise';
        $scope.FOLD_COMMAND = 'fold';
        $scope.LEAVE_COMMAND = 'leave';
        $scope.CHECK_COMMAND = 'check';

        //max time for user's action
        $scope.MAX_TIME = 130;

        //number of players
        $scope.players_amount = 0;

        //user's index
        $scope.user_index = 0;

        //card prototype
        $scope.card = {
            face: 'A',
            suit: 'Spades'
        };

        $scope.back_of_card = {
            first_card: {
                face: 'back',
                suit: 'card'
            },
            second_card: {
                face: 'back',
                suit: 'card'
            }
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
            return Array.max( $scope.players_contribution );
        };

        //------------------- cards on the center: flop, river, turn ---
        //values

        //$scope.$watch('players_name[0]', function(newVal, oldVal){
        //    if(newVal != oldVal){
        //        $scope.players_name[0] = newVal;
        //        $scope.is_players_visible[0] = true;
        //    }
        //
        //});


        $scope.flop = [
            $scope.back_of_card.first_card,
            $scope.back_of_card.first_card,
            $scope.back_of_card.first_card
            ];
        $scope.flop.is_visible = false;

        $scope.turn = {
            face: $scope.back_of_card.first_card.face,
            suit: $scope.back_of_card.first_card.suit
        };
        $scope.turn.is_visible = false;

        $scope.river = {
            face: $scope.back_of_card.first_card.face,
            suit: $scope.back_of_card.first_card.suit
        };
        $scope.river.is_visible = false;

        //------------------- players ----------------------------------
        $scope.is_players_visible = [
            false, false, false, false, false, false
        ];
        $scope.is_card_visible = [
            false, false, false, false, false, false
        ];

        $scope.dealer = -1;
        $scope.big_blind = -1;
        $scope.small_blind = -1;

        $scope.game_has_started = true;

        $scope.is_hand_power_visible = false;

        $scope.players_turn = [
            false, false, false, false, false, false
        ];

        $scope.is_user_ready = false;

        $scope.players_index_turn = 0;

        $scope.players_name = [
            '', '', '', '', '', ''
        ];

        $scope.back_of_card = {
            first_card: {
                face: 'back',
                suit: 'card'
            },
            second_card: {
                face: 'back',
                suit: 'card'
            }
        };

        $scope.players_cards = [
            {
                first_card: {
                    face: 'back',
                    suit: 'card'
                },
                second_card: {
                    face: 'back',
                    suit: 'card'
                }
            },
            {
                first_card: {
                    face: 'back',
                    suit: 'card'
                },
                second_card: {
                    face: 'back',
                    suit: 'card'
                }
            },
            {
                first_card: {
                    face: 'back',
                    suit: 'card'
                },
                second_card: {
                    face: 'back',
                    suit: 'card'
                }
            },
            {
                first_card: {
                    face: 'back',
                    suit: 'card'
                },
                second_card: {
                    face: 'back',
                    suit: 'card'
                }
            },
            {
                first_card: {
                    face: 'back',
                    suit: 'card'
                },
                second_card: {
                    face: 'back',
                    suit: 'card'
                }
            },
            {
                first_card: {
                    face: 'back',
                    suit: 'card'
                },
                second_card: {
                    face: 'back',
                    suit: 'card'
                }
            }
        ];

        $scope.user_remaining_time = [

        ];

        $scope.user_contribution = '';

        $scope.user_odds = {
            win: '',
            draw: '',
            lose: ''
        };

        $scope.players_contribution = [
        ];

        $scope.total_pot_value = '';

        $scope.players_stack = [
        ];

        $scope.players_bet = [
        ];

        $scope.players_turn = {

        };

        $scope.is_players_ready = [

        ];

        $scope.user_bet = '';


        $scope.updatePotValue = function(){
            $scope.total_pot_value = 0;
            for(var val in $scope.players_contribution)
                $scope.total_pot_value += val;
        };


        //------------------- buttons ---------------------------------
        $scope.sit = {
            button_disabled: false,
            status: false
        };
        $scope.stand = {
            button_disabled: true,
            status: false
            };
        $scope.call = {
            button_disabled: false,
            status: false
        };
        $scope.check = {
            button_disabled: false,
            status: false
        };
        $scope.raise = {
            button_disabled: false,
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
            button_disabled: true,
            status: false,
        };
        $scope.login = {
            button_disabled: false,
            status: false
        };

        //checks if any button should be disabled
        $scope.checkButtons = function() {

            // TO DO //////
            //ready
            $scope.game_has_started == true ? $scope.ready.button_disabled = true : $scope.ready.button_disabled = false;
            //stand up
            $scope.game_has_started == true ? $scope.stand.button_disabled = false : $scope.stand.button_disabled = true;
            //call
            $scope.is_user_turn == true && $scope.is_logged == true ? $scope.call.button_disabled = false : $scope.call.button_disabled = true;
            //check
            $scope.is_user_turn == true && $scope.is_logged == true ? $scope.check.button_disabled = false : $scope.check.button_disabled = true;
            //bet
            $scope.is_user_turn == true && $scope.is_logged == true ? $scope.bet.button_disabled = false : $scope.bet.button_disabled = true;
            //raise
            $scope.is_user_turn == true && $scope.is_logged == true ? $scope.raise.button_disabled = false : $scope.raise.button_disabled = true;
            //fold
            $scope.is_user_turn == true && $scope.is_logged == true ? $scope.fold.button_disabled = false : $scope.fold.button_disabled = true;

        };

        //--------------------chat and game history--------------------
        $scope.chat_entries = [];
        $scope.entry = '';
        $scope.is_logged = false;

        $scope.user_login = '';
        $scope.new_entry = '';


        $scope.setLogin = function () {
            //connect and send initial login data package
            if ($scope.user_login.length > 1 && $scope.user_login.length <= 10 && $scope.socket.readyState === 1){
                $scope.sendResponse($scope.user_login);
                $scope.is_logged = true;
            }
        };

        $scope.setTurn = function () {
            $scope.is_user_turn == false ? $scope.is_user_turn = true : $scope.is_user_turn = false;
        };

        $scope.setReady = function (){
            $scope.is_user_ready = true;
            $scope.sendResponse($scope.READY_COMMAND);
        };

        $scope.setCheck = function (){
            $scope.sendResponse($scope.CHECK_COMMAND);
        };

        $scope.setCall = function (){
            $scope.user_contribution = $scope.getMax();
            $scope.sendResponse($scope.CALL_COMMAND);
        };

        $scope.setBet = function() {
            if($scope.user_bet > 0 && $scope.user_bet < 9999  && $scope.socket.readyState === 1){
                $scope.sendResponse($scope.BET_COMMAND + " " + $scope.user_bet);
                $scope.user_bet = '';
            }
        };

        $scope.setRaise = function() {
            if($scope.user_bet.length > 0  && $scope.socket.readyState === 1) {
                $scope.sendResponse($scope.RAISE_COMMAND + " " + $scope.user_bet);
                $scope.user_bet = '';
            }
        };

        $scope.setStand = function(){
            $scope.sendResponse($scope.LEAVE_COMMAND);
        };

        $scope.addChatEntry = function (){
            if($scope.new_entry !== ''  && $scope.new_entry !== undefined) {
                $scope.chat_entries.push({
                    string: $scope.new_entry,
                    author: $scope.user_login,
                    dt: new Date()
                });
                $scope.new_entry = '';
            }
        };

        //----------------- updating data -----------------------------
        $scope.update = function (new_data){

            $scope.$apply( function() {

                //temp
                var result = '';
                var counter = 0;

                //number of players
                $scope.players_amount = Number(new_data.players_number);

                //updating players' attributes
                for (var i = 0; i < $scope.players_amount; ++i) {
                    if (new_data[i]) {
                        result = new_data[i].split(" ");
                        counter = 0;

                        //players' names
                        $scope.players_name[i] = result[0];
                        $scope.is_players_visible[i] = true;

                        console.log("widoczny", $scope.is_players_visible[i]);

                        //players' cards -> if 'None' then display back of the card (unknown state)
                        if (result[1] == 'None') {
                            $scope.players_cards[i].first_card = $scope.back_of_card.first_card;
                            $scope.players_cards[i].second_card = $scope.back_of_card.first_card;
                            $scope.is_card_visible[i] = false;
                            counter = 3;
                        } else {
                            $scope.players_cards[i].first_card.face = result[1];
                            $scope.players_cards[i].first_card.suit = result[2];
                            $scope.players_cards[i].second_card.suit = result[3];
                            $scope.players_cards[i].second_card.suit = result[4];
                            $scope.is_card_visible[i] = true;
                            counter = 5;
                        }

                        //players' ready states
                        result[counter++].toLowerCase() == 'true' ? $scope.is_players_ready[i] = true : $scope.is_players_ready[i] = false;

                        //players' turn
                        result[counter++].toLowerCase() == 'true' ? $scope.players_turn[i] = true : $scope.players_turn[i] = false;

                        //players' leaving states TO DO //////////////////////////////
                        counter++;

                        //players' stacks
                        $scope.players_stack[i] = Number(result[counter++]);

                        //players' latest contribution to pot
                        $scope.players_contribution[i] = Number(result[counter++]);
                        if ($scope.players_contribution[i])
                            $scope.game_has_started = true;

                        //user's index on the table
                        $scope.user_index = Number(new_data.index);

                        if ($scope.players_turn[$scope.user_index] === true)
                            $scope.is_user_turn = true;
                        else
                            $scope.is_user_turn = false;

                        console.log($scope.players_cards[i].first_card, $scope.players_cards[i].second_card, $scope.is_players_ready[i], $scope.is_players_ready[i], $scope.players_stack[i], $scope.players_contribution[i], $scope.user_index);
                    }
                }

                //board cards
                if (new_data.table_card_0 == 'None') {
                    $scope.flop[0] = $scope.back_of_card.first_card;
                    $scope.flop.is_visible = false;
                } else {
                    $scope.flop[0].face = new_data.table_card_0.split[" "][0];
                    $scope.flop[0].suit = new_data.table_card_0.split[" "][1];
                    $scope.flop.is_visible = true;
                }

                if (new_data.table_card_1 == 'None') {
                    $scope.flop[1] = $scope.back_of_card.first_card;
                } else {
                    $scope.flop[1].face = new_data.table_card_1.split[" "][0];
                    $scope.flop[1].suit = new_data.table_card_1.split[" "][1];
                }

                if (new_data.table_card_2 == 'None') {
                    $scope.flop[2] = $scope.back_of_card.first_card;
                } else {
                    $scope.flop[2].face = new_data.table_card_2.split[" "][0];
                    $scope.flop[2].suit = new_data.table_card_2.split[" "][1];
                }

                if (new_data.table_card_3 == 'None') {
                    $scope.turn.face = $scope.back_of_card.first_card.face;
                    $scope.turn.suit = $scope.back_of_card.first_card.suit;
                    $scope.turn.is_visible = false;
                } else {
                    $scope.turn.face = new_data.table_card_3.split[" "][0];
                    $scope.turn.suit = new_data.table_card_3.split[" "][1];
                    $scope.turn.is_visible = true;
                }

                if (new_data.table_card_4 == 'None') {
                    $scope.river.face = $scope.back_of_card.first_card.face;
                    $scope.river.suit = $scope.back_of_card.first_card.suit;
                    $scope.river.is_visible = false;
                } else {
                    $scope.river.face = new_data.table_card_4.split[" "][0];
                    $scope.river.suit = new_data.table_card_4.split[" "][1];
                    $scope.river.is_visible = true;
                }

                //dealer's index
                if (new_data.dealer != null) {
                    $scope.dealer = new_data.dealer;
                    $scope.big_blind = ($scope.dealer + 2) % ($scope.players_amount);
                    $scope.small_blind = ($scope.dealer + 1) % ($scope.players_amount);
                } else {
                    $scope.dealer = -1;
                    $scope.big_blind = -1;
                    $scope.small_blind = -1;
                }

                //winning odds
                $scope.user_odds.win = new_data.win;
                $scope.user_odds.draw = new_data.draw;
                $scope.user_odds.lose = new_data.lose;

                //update the buttons
                console.log("apply");

                $scope.checkButtons();
            })

        };


        //----------------- server connection -------------------------

        $scope.message_server = {
            content: ''
        };


        $scope.socket.onopen = function(e) {
            console.log("opened connection");
        };

        $scope.socket.onmessage = function(e) {
            console.log(e.data);
            $scope.update(JSON.parse(e.data));
        };

        $scope.socket.onclose = function(e) {
            console.log("closed");
        };


        //----------------- sending a response to server --------------

        $scope.sendResponse = function(key){
            //checking connection state
            if($scope.socket.readyState === 1){
                $scope.message_server.content = key;
                console.log(key);
                $scope.socket.send(JSON.stringify($scope.message_server));
            }
        };

    });