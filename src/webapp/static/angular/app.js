'use strict';

var app = angular.module("AngularFlask", ["ngRoute",'ngMaterial', 'ngMessages', 'ui.bootstrap','ngSanitize', 'ngCookies']);
app.config(function ($routeProvider) {

    $routeProvider
        .when("/", {
            templateUrl: 'static/partials/display_data.html?v=1',
            controller: IndexController
        })
        .when("/show-history", {
            templateUrl: "static/partials/show_history.html",
            controller: HistoryController
        })
        .otherwise({
            redirectTo: '/'
    });
});
