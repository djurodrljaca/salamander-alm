'use strict';

// Declare app level module which depends on views, and components
angular.module('webuiApp', [
  'ngRoute',
  'webuiApp.view1',
  'webuiApp.view2',
  'webuiApp.version'
]).
config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
  $locationProvider.hashPrefix('!');

  $routeProvider.otherwise({redirectTo: '/view1'});
}]);
