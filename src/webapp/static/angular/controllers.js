'use strict';

/* Controllers */
app.controller('login_controller', function($scope, $http, $cookies) {
    $scope.user_dict = {};
    $http({
            method: 'GET',
            url: '/get-login-info/',
        }).then(function (response) {
            $scope.user_dict = response.data;
            if ($scope.user_dict.role==='admin'){
                $scope.is_admin=true;
            }
            $cookies.put('role', $scope.user_dict.role);

        }, function (error) {
            console.log(error);
        }).finally(function () {
        });
});

function IndexController($scope, $http, $sce, $mdDialog, $timeout, $location, $cookies) {
    $scope.case_dict = {};
    $scope.parties_dict = {};
    $scope.potential_dict = {};
    $scope.party_potential_list_dict = {};
    $scope.phone_field_list = [];
    $scope.party_div_visible = true;
    $scope.show_is_actual = false;
    $scope.have_case = true;
    $scope.hidden_party_id = null;
    $scope.hidden_potential_id = null;
    $scope.index = $scope.phone_field_list.length;
    $scope.party_div_spinner_load= true;
    $scope.trustSrc = function (src) {
        return $sce.trustAsResourceUrl(src);
    };
    if ($cookies.get('role')==='staff'){$scope.is_staff_user=true;}
    $scope.get_cases = function () {
        if ($scope.case_dict.status===null){
            return
        }
        $scope.post_data = {
            'next_item_index': $scope.case_dict.next_item_index,
            'process_case_id': $scope.case_dict.id,
            'case_key': $scope.case_dict.case_key,
            'is_collectible': $scope.case_dict.is_collectible,
            'document_id': $scope.case_dict.document_id,
            'status': $scope.case_dict.status,
        };
        $scope.show_loader = true;
        $scope.case_dict.document_url = '//';
        $http({
            method: 'POST',
            url: '/get-cases',
            data: $scope.post_data,
            timeout: 20000
        }).then(function (response) {
            let response_dict =response.data.data;
            if (!response_dict){
                $scope.have_case = false;
                $scope.showAlert('Cases Got Over.', '');
                return
            }
            $scope.case_dict = response_dict;
            let file_name = $scope.case_dict.file_path;
            if(file_name.includes('.tif')){$scope.show_file_name=true;}
            if ($cookies.get('role')==='staff'){$scope.case_dict.status=null;}
        }, function (error) {
            if(error.status===307){
                $scope.showAlert('You do not have user settings..!','Please contact to admin');
                $scope.have_case = false;
            }
            $scope.showAlert('There is some issue in getting cases..!!');
            console.log(error);
        }).finally(function () {
            $scope.show_loader = false;
            $scope.parties_dict={'page':0};
            $scope.get_parties();
        });
    };
    $scope.get_cases();

    $scope.get_parties = function (load_more) {
        if (!$scope.case_dict.case_key){
            return
        }
        $scope.post_data = {
            'page': $scope.parties_dict.page + 1 ,
            'case_key': $scope.case_dict.case_key
        };
         $scope.load_btn_isDisabled=true;
        if (!load_more){$scope.load_parties_spinner = true;}else{$scope.load_parties_btn_spinner = true;}
        $http({
            method: 'POST',
            url: '/get-parties',
            data: $scope.post_data,
            timeout: 20000
        }).then(function (response) {
            let response_dict =response.data.data;
            if (response.data.status === 'FAILURE') {$scope.showAlert('There is some issue in fetching parties..!!');return}
            if ($scope.post_data.page ===1 ){
                if (response_dict.parties.length===0){
                    $scope.showAlert('There is some issue in fetching parties..!!');
                    return
                }
                $scope.parties_dict = response_dict;
            }else{
                $scope.parties_dict.items_per_page = response_dict.items_per_page;
                $scope.parties_dict.page = response_dict.page;
                $scope.parties_dict.parties = $scope.parties_dict.parties.concat(response_dict.parties);
            }
            if($scope.ObjectLength($scope.parties_dict.parties)<$scope.parties_dict.total_matches){
                $scope.has_more_party = true;
            }else{
                $scope.has_more_party = false;
            }
        }, function (error) {
            $scope.showAlert('There is some issue in fetching parties..!!');
            console.log(error);
        }).finally(function () {
            $scope.load_parties_spinner = $scope.load_btn_isDisabled=$scope.load_parties_btn_spinner=false;
        });
    };

    $scope.get_party_potential = function (party_id, should_refresh=false) {
        if ($scope.post_data.party_id && !should_refresh) {
            if ($scope.post_data.party_id === party_id) {
                return
            }
        }
        $scope.post_data = {
            'case_key': $scope.case_dict.case_key,
            'party_id': party_id,
        };
        $scope.load_potential_spinner =  true;
        $scope.add_btn_on_load = false;
        $scope.party_potential_list_dict={};
        $http({
            method: 'POST',
            url: '/get-party-potential',
            data: $scope.post_data,
            timeout: 20000
        }).then(function (response) {
            let response_dict =response.data.data;
            if (response.status === 'FAILURE') { $scope.showAlert(); return}
            if (response.data.status === 'FAILURE') { $scope.showAlert(); return}

            $scope.party_potential_list_dict = response_dict.potential_info_dict;
        }, function (error) {
            $scope.party_potential_list_dict={};
            $scope.showAlert();
            console.log(error);
        }).finally(function () {
            $scope.load_potential_spinner = false;
            if ($cookies.get('role')==='staff'){$scope.add_btn_on_load=true;}
        });
    };
    $scope.showAlert = function (title='There is some issue to get parties Potential.',content='Please contact to admin') {
        $mdDialog.show(
            $mdDialog.alert()
                .parent(angular.element(document.querySelector('#popupContainer')))
                .title(title)
                .textContent(content)
                .ok('Ok')
        );
    };
    $scope.add_phone_field = function () {
        var newItemNo = ++$scope.index;
        $scope.phone_field_list.push({'id': newItemNo});
    };

    $scope.edit_potential = function (potential_id, party_id, party_fullname) {
        $scope.party_fullname = party_fullname;
        $scope.hidden_party_id = party_id;
        $scope.hidden_potential_id = potential_id;
        $scope.party_div_visible =false;
        $scope.potential_div_visible =true;
        if ($cookies.get('role')!=='staff'){$scope.disabled_form=true;}
        function update_disable_field() {
            $scope.should_disable_address= true;
            $scope.should_disable_city= true;
            $scope.should_disable_state= true;
            $scope.should_disable_zipcode= true;
        }

        Object.keys($scope.party_potential_list_dict.potentials).forEach(function (key) {
            if ($scope.party_potential_list_dict.potentials[key].potential_id === potential_id) {
                $scope.potential_dict = $scope.party_potential_list_dict.potentials[key];
                $scope.phone_field_list = $scope.potential_dict.phones;
                if ($scope.potential_dict.email !=''){$scope.is_email_visible = true;}
                if ($scope.potential_dict.source =='WHITEPAGES'){
                    update_disable_field();
                    $scope.show_is_actual = true;
                }else if ($scope.potential_dict.source =='PARSED FROM DOCUMENT'){
                    update_disable_field();
                    $scope.should_disable_is_actual= true;
                }
            }
        });
    };
    $scope.add_potential = function (party_id, party_fullname) {
        $scope.is_email_visible = false;
        $scope.party_fullname = party_fullname;
        $scope.hidden_party_id = party_id;
        $scope.hidden_potential_id = null;
        $scope.show_is_actual = false;
        $scope.party_div_visible = false;
        $scope.potential_div_visible = true;
        $scope.potential_dict = {};
        $scope.phone_field_list = [];
        $scope.potential_dict.court_verified = 'yes';
    };

    $scope.save_potential = function () {
        $scope.post_data = {
            'process_case_id': $scope.case_dict.id,
            'case_key': $scope.case_dict.case_key,
            'dynamo_document_id': $scope.case_dict.dynamo_document_id,
            'codaxtr_party_id': $scope.hidden_party_id,
            'potential_id': $scope.hidden_potential_id,
            'potential': $scope.potential_dict,
            'phone': $scope.phone_field_list,
            'party_fullname': $scope.party_fullname,
        };
        $http({
            method: 'POST',
            url: '/save-potential',
            data: $scope.post_data
        }).then(function (response) {
            if (response.data.status.toUpperCase() === 'FAILURE') {
                if (response.data.type==='POTENTIAL_EXISTS'){
                    $scope.showAlert('Address already Exists..', ' ');
                }else{
                    $scope.showAlert('Error ',response.data.message);
                }
                return
            }
            $scope.success_message = true;
            $timeout(function() {$scope.success_message = false;}, 3000);
            $scope.get_party_potential($scope.hidden_party_id, true);
            $scope.potential_div_visible=false;
            $scope.party_div_visible=true;
        }, function (error) {
            $scope.showAlert();
            console.log(error);
        });
    };

    $scope.comment_form = function () {
        $scope.post_data = {
            'parent_comment_id': $scope.parent_comment_id,
            'process_case_id': $scope.case_dict.id,
            'comment': $scope.comment
        };
        $http({
            method: 'POST',
            url: '/save-comments',
            data: $scope.post_data
        }).then(function (response) {
            $scope.comment='';
            $scope.comment_msg=true;
             $timeout(function() {$scope.comment_msg = false;}, 3000);
        }, function (error) {
            console.log(error);
        });
    };

    $scope.get_comments = function () {
        $scope.post_data = {
            'process_case_id': $scope.case_dict.id
        };
        $http({
            method: 'POST',
            url: '/fetch-comments',
            data: $scope.post_data
        }).then(function (response) {
            console.log(response);
            $scope.comments_form=response.data;
        }, function (error) {
            console.log(error);
        });
    };


    /**
     * @return {number}
     */
    $scope.ObjectLength = function(object_data){
       return Object.keys(object_data).length;
    }
}

function HistoryController($scope, $http) {
    $scope.history_info = {};

    $scope.get_history = function () {
        $http({
            method: 'POST',
            url: '/get-history',
            data: $scope.history_info
        }).then(function (response) {
            console.log(response)
            $scope.history_info = response.data.data;
        }, function (error) {
            console.log(error);
        });
    };
    $scope.get_history();
}
