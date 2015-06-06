
'use strict';

//var socket = new WebSocket("ws://localhost:10000/");

angular.module('PokerMain', [])
    .controller('PokerCtrl', ["$scope", function($scope) {

        //server settings
        $scope.host = 'localhost';
        $scope.port = 10000;
        $scope.connection_string = "ws://" + $scope.host + ":" + $scope.port + "/";

        //setting up a connection
        var socket = new WebSocket($scope.connection_string);

        //command texts
        $scope.READY_COMMAND = 'start';
        $scope.CALL_COMMAND = 'call';
        $scope.BET_COMMAND = 'bet';
        $scope.RAISE_COMMAND = 'raise';
        $scope.FOLD_COMMAND = 'fold';
        $scope.LEAVE_COMMAND = 'leave';
        $scope.CHECK_COMMAND = 'check';
        $scope.CHAT_COMMAND = 'chat';

        //max players
        $scope.MAX_PLAYERS = 6;

        //card prototype
        $scope.card = {
            face: '',
            suit: ''
        };

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

        //------------------- cards on the center: flop, river, turn --
        //initial values of board cards
        $scope.flop = [
            {face: 'back', suit: 'card'},
            {face: 'back', suit: 'card'},
            {face: 'back', suit: 'card'}
            ];
        $scope.flop.is_visible = false;
        $scope.turn = {face: 'back', suit: 'card'};
        $scope.turn.is_visible = false;
        $scope.river = {face: 'back', suit: 'card'};
        $scope.river.is_visible = false;

        //------------------- user ------------------------------------
        $scope.is_user_ready = false;
        $scope.user_index = undefined;
        $scope.user_remaining_time = '';
        $scope.user_contribution = '';
        $scope.user_login = '';
        $scope.user_bet = '';
        $scope.is_user_turn = false;
        $scope.is_logged = false;
        $scope.is_hand_power_visible = false;
        $scope.user_odds = {
            win: '',
            draw: '',
            loss: ''
        };

        //------------------- players ---------------------------------
        //filled with initial values
        $scope.players_amount = -1;
        $scope.max_contribution = -1;
        $scope.dealer = -1;
        $scope.big_blind = -1;
        $scope.small_blind = -1;
        $scope.game_has_started = false;
        $scope.is_players_visible = [
            false, false, false, false, false, false
        ];
        $scope.is_card_visible = [
            false, false, false, false, false, false
        ];
        $scope.players_turn = [
            false, false, false, false, false, false
        ];
        $scope.players_name = [];
        //initial values
        $scope.players_cards = [
            {first_card: {face: 'back',suit: 'card'}, second_card: {face: 'back', suit: 'card'}},
            {first_card: {face: 'back',suit: 'card'}, second_card: {face: 'back', suit: 'card'}},
            {first_card: {face: 'back',suit: 'card'}, second_card: {face: 'back', suit: 'card'}},
            {first_card: {face: 'back',suit: 'card'}, second_card: {face: 'back', suit: 'card'}},
            {first_card: {face: 'back',suit: 'card'}, second_card: {face: 'back', suit: 'card'}},
            {first_card: {face: 'back',suit: 'card'}, second_card: {face: 'back', suit: 'card'}}
        ];
        $scope.players_contribution = [];
        $scope.players_stack = [];
        $scope.is_players_folded = [];
        $scope.is_players_ready = [];
        $scope.total_pot_value = 0;
        
        $scope.chat_entries = [];
        $scope.entry = '';
        $scope.new_entry = '';
        $scope.addChatEntry = function () {
            //send to server
            if($scope.new_entry){
                var time = new Date();
                $scope.sendResponse($scope.CHAT_COMMAND + " " + $scope.user_login + "&" + $scope.new_entry + "&" + time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds());
                $scope.new_entry = '';
            }
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
            button_disabled: false,
            status: false
        };
        $scope.bet = {
            button_disabled: false,
            status: false
        };
        $scope.login = {
            button_disabled: false,
            status: false
        };
        $scope.allin = {
            button_disabled: false,
            status: false
        };

        //--------------------buttons' click effect--------------------

        $scope.setLogin = function () {
            //connect and send initial login data package
            if ($scope.user_login.length > 1 && $scope.user_login.length <= 10 && socket.readyState === 1){
                $scope.sendResponse($scope.user_login);
                $scope.is_logged = true;
                $scope.ready.button_disabled = false;
            }
        };
        $scope.setTurn = function () {
            $scope.is_user_turn === false ? $scope.is_user_turn = true : $scope.is_user_turn = false;
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
        $scope.setFold = function(){
            $scope.sendResponse($scope.FOLD_COMMAND);
        };
        $scope.setBet = function() {
            if($scope.checkIfCanBet() && Number($scope.user_bet) < $scope.players_stack[$scope.user_index]) {
                $scope.sendResponse($scope.BET_COMMAND + " " + $scope.user_bet);
                $scope.user_bet = '';
            }
        };
        $scope.setAllIn = function() {
                //if player's stack is bigger than max on the table
                if($scope.checkIfCanBet()) {
                    //send bet
                    $scope.user_bet = $scope.players_stack[$scope.user_index];
                    if ($scope.getMax() === $scope.players_contribution[$scope.user_index])
                        $scope.sendResponse($scope.BET_COMMAND + " " + $scope.user_bet);
                    else
                        $scope.sendResponse($scope.RAISE_COMMAND + " " + $scope.user_bet);
                    $scope.user_bet = '';
                }
                //send call
                else {
                    $scope.sendResponse($scope.CALL_COMMAND);
                    $scope.user_bet = '';
                }
        };
        $scope.setRaise = function() {
            if($scope.checkIfCanBet() && Number($scope.user_bet) < $scope.players_stack[$scope.user_index]) {

                $scope.sendResponse($scope.RAISE_COMMAND + " " + $scope.user_bet);
                $scope.user_bet = '';
            }
        };
        $scope.setStand = function(){
            $scope.sendResponse($scope.LEAVE_COMMAND);
            //set all of the button disabled
            $scope.stand.button_disabled = true;
            $scope.call.button_disabled = true;
            $scope.ready.button_disabled = true;
            $scope.bet.button_disabled = true;
            $scope.raise.button_disabled = true;
            $scope.allin.button_disabled = true;
            $scope.fold.button_disabled = true;
            $scope.check.button_disabled = true;
            $scope.kickFromGame();
        };
        //----------------- data update from server -------------------
        $scope.update = function (new_data){
            $scope.$apply( function() {
                //temp variables
                var result = '';
                var counter = 0;

                //number of players
                $scope.players_amount = Number(new_data.playersnumber);

                //total pot value
                $scope.total_pot_value = 0;

                //updating players' attributes
                for (var i = 0; i < $scope.MAX_PLAYERS; ++i) {
                    if (new_data[i]) {
                        result = new_data[i].split(" ");
                        counter = 0;

                        //players' names
                        $scope.players_name[i] = result[0];
                        $scope.is_players_visible[i] = true;

                        //players' cards -> if 'None' then display back of the card (unknown state)
                        if (result[1] == 'None') {
                            $scope.players_cards[i].first_card = {face: 'back', suit: 'card'};
                            $scope.players_cards[i].second_card = {face: 'back', suit: 'card'};
                            $scope.is_card_visible[i] = false;
                            counter = 3;
                        } else {
                            $scope.players_cards[i].first_card.face = result[1];
                            $scope.players_cards[i].first_card.suit = result[2];
                            $scope.players_cards[i].second_card.face = result[3];
                            $scope.players_cards[i].second_card.suit = result[4];
                            $scope.is_card_visible[i] = true;
                            counter = 5;
                        }

                        //players' ready states
                        result[counter++].toLowerCase() == 'true' ? $scope.is_players_ready[i] = true : $scope.is_players_ready[i] = false;

                        //players' turn
                        result[counter++].toLowerCase() == 'true' ? $scope.players_turn[i] = true : $scope.players_turn[i] = false;

                        //players' leaving state
                        result[counter++].toLowerCase() == 'true' ? $scope.is_players_folded[i] = true : $scope.is_players_folded[i] = false;

                        //players' stacks
                        $scope.players_stack[i] = Number(result[counter++]);

                        //players' latest contribution to pot
                        $scope.players_contribution[i] = Number(result[counter++]);

                        //adding to the pot
                        if($scope.players_contribution[i])
                            $scope.total_pot_value += $scope.players_contribution[i];

                        //user's index on the table
                        $scope.user_index = Number(new_data.index);

                        //checking if it is user's turn
                        if ($scope.players_turn[$scope.user_index] === true && $scope.is_user_turn === false){
                            $scope.is_user_turn = true;
                        }
                        else if($scope.players_turn[$scope.user_index] === false && $scope.is_user_turn === true)
                            $scope.is_user_turn = false;
                    }
                    else
                        $scope.is_players_visible[i] = false;
                }
                //game status
                !new_data.gamestarted && $scope.game_has_started ? $scope.kickFromGame() :
                new_data.gamestarted && !$scope.game_has_started ? $scope.game_has_started = true : $scope.game_has_started = new_data.gamestarted;

                //board cards
                if (new_data.tablecard0 == "None") {
                    $scope.flop[0] = {face: 'back', suit: 'card'};
                    $scope.flop[1] = {face: 'back', suit: 'card'};
                    $scope.flop[2] = {face: 'back', suit: 'card'};
                    $scope.flop.is_visible = false;
                } else {
                    $scope.flop.is_visible = true;

                    result = new_data.tablecard0.split(" ");
                    $scope.flop[0].face = result[0];
                    $scope.flop[0].suit = result[1];

                    result = new_data.tablecard1.split(" ");
                    $scope.flop[1].face = result[0];
                    $scope.flop[1].suit = result[1];

                    result = new_data.tablecard2.split(" ");
                    $scope.flop[2].face = result[0];
                    $scope.flop[2].suit = result[1];
                }
                if (new_data.tablecard3 == 'None') {
                    $scope.turn.face = 'back';
                    $scope.turn.suit = 'card';
                    $scope.turn.is_visible = false;
                } else {
                    result = new_data.tablecard3.split(" ");
                    $scope.turn.face = result[0];
                    $scope.turn.suit = result[1];
                    $scope.turn.is_visible = true;
                }
                if (new_data.tablecard4 == 'None') {
                    $scope.river.face = 'back';
                    $scope.river.suit = 'card';
                    $scope.river.is_visible = false;
                } else {
                    result = new_data.tablecard4.split(" ");
                    $scope.river.face = result[0];
                    $scope.river.suit = result[1];
                    $scope.river.is_visible = true;
                }
                //dealer's index
                if (new_data.dealer != null) {
                    $scope.dealer = new_data.dealer;
                    if ($scope.players_amount === 2) {
                        $scope.big_blind = ($scope.dealer + 1) % ($scope.players_amount);
                        $scope.small_blind = ($scope.dealer);
                    }
                    else {
                        $scope.big_blind = ($scope.dealer + 2) % ($scope.players_amount);
                        $scope.small_blind = ($scope.dealer + 1) % ($scope.players_amount);
                    }
                } else {
                    $scope.dealer = -1;
                    $scope.big_blind = -1;
                    $scope.small_blind = -1;
                }

                //winning odds
                $scope.user_odds.win = new_data.win.toFixed(2);
                $scope.user_odds.draw = new_data.draw.toFixed(2);
                $scope.user_odds.loss = new_data.loss.toFixed(2);

                //update 'stand up' button state
                $scope.game_has_started == true ? $scope.stand.button_disabled = false : $scope.stand.button_disabled = true;
                $scope.max_contribution = $scope.getMax();

                $scope.checkButtonsState();

                //update chat
                if(new_data.chat != null)
                    $scope.updateChatEntries(new_data.chat);
            })
        };

            //update playing buttons states
        $scope.checkButtonsState = function(){
            if($scope.players_stack[$scope.user_index] + $scope.players_contribution[$scope.user_index] < $scope.getMax()){
                $scope.bet.button_disabled = true;
                $scope.check.button_disabled = true;
                $scope.raise.button_disabled = true;
                $scope.call.button_disabled = true;
            }
            else if($scope.getMax() > $scope.players_contribution[$scope.user_index] && $scope.players_stack[$scope.user_index] + $scope.players_contribution[$scope.user_index] >= $scope.getMax()) {
                $scope.bet.button_disabled = true;
                $scope.check.button_disabled = true;
                $scope.raise.button_disabled = false;
                $scope.call.button_disabled = false;
            }
            else if(!$scope.flop.is_visible){
                $scope.bet.button_disabled = true;
                $scope.check.button_disabled = false;
                $scope.raise.button_disabled = false;
                $scope.call.button_disabled = true;
            }
            else{
                $scope.bet.button_disabled = false;
                $scope.check.button_disabled = false;
                $scope.raise.button_disabled = true;
                $scope.call.button_disabled = true;
            }
        };

        $scope.updateChatEntries = function (val) {
                var result = val.split("&");
                $scope.chat_entries.push({
                    author: result[0],
                    string: result[1],
                    dt: result[2]
                });
            var textarea = document.getElementById('scrollable');
            textarea.scrollTop = textarea.scrollHeight;
        };

        $scope.checkIfCanBet = function(){
            return (($scope.players_contribution[$scope.user_index] + $scope.players_stack[$scope.user_index]) > $scope.getMax());
        };
        //stops game after wrong input
        $scope.kickFromGame = function(){
            alert("You have been disconnected");
        };

        //----------------- server connection -------------------------
        //server message prototype
        $scope.message_server = {
            content: ''
        };
        socket.onopen = function(e) {
        };
        socket.onmessage = function(e) {
            $scope.update(JSON.parse(e.data));
        };
        socket.onclose = function(e) {
            alert("You have been disconnected");
        };

        //----------------- response to server ------------------------
        $scope.sendResponse = function(key){
            //checking connection state
            if(socket.readyState === 1){
                $scope.message_server.content = key;
                socket.send(JSON.stringify($scope.message_server));
            }
        };
    }]);
