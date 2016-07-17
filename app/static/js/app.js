console.log("{{msg}}")

angular.module('app', ['ngRoute', 'ngFileUpload', 'ngSanitize'])


.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[').endSymbol(']}')
})


.controller('mainController', ['$scope', '$http','$filter', '$timeout', '$sce', 'Upload', function($scope, $http, $filter, $timeout, $sce, Upload) {
  console.log("Loading Main controller")

  $scope.trustSrc = function(src) {
    return $sce.trustAsResourceUrl(src);
  }


  if (msg) {
    $scope.message = msg;
  } else {
    $scope.message = "Unknown"
  }



  $scope.uploadFiles = function(file, errFiles) {
    $scope.f = file;
    $scope.errFile = errFiles && errFiles[0];
    if (file) {
      file.upload = Upload.upload({
        url: '/upload',
        data: {file: file}
      });

      file.upload.then(function (response) {
        $timeout(function () {
          console.log(response)
          file.result = response.data;
          $("body").animate({scrollTop: $('.marketing').offset().top}, "slow");
        });
      }, function (response) {
        if (response.status > 0)
          console.log(response)
          $scope.errorMsg = response.status + ': ' + response.data;
      }, function (evt) {
        file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
      });
    }   
  }
  // $scope.readURL = function() {
  //   console.log("-- change")
  // }

  // function readURL(input) {
  //     if (input.files && input.files[0]) {
  //         var reader = new FileReader();
          
  //         reader.onload = function (e) {
  //             $('#blah').attr('src', e.target.result);
  //         }
          
  //         reader.readAsDataURL(input.files[0]);
  //     }
  // }
  
  // $("#item1").change(function(){
  //   console.log("CHANGE")
  //   readURL(this);
  // });

}])