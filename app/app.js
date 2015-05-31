// Declare app level module which depends on views, and components
angular.module('PokerMain', [

])

.controller('PokerMainCtrl', function($scope){
        $scope.version = 0.1;
        $scope.card_types = [
        ];

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
            false, false, false, false, false, false
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
        };$scope.ready = {
            button_disabled: false,
            status: false
        };$scope.fold = {
            button_disabled: true,
            status: false
        };


        //


    })
;
