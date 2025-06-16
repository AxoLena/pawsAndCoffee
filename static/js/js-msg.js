$(document).ready(function(){
    var successMessage = $("#jq-notification-success");
    var showMsg = localStorage.getItem('successMsgText');
    var msg = localStorage.getItem('msg');
    if(msg === 'true'){
        successMessage.html(showMsg);
        successMessage.fadeIn(400);
        setTimeout(function () {
            successMessage.fadeOut(400);
        }, 3000);
        localStorage.setItem('msg', 'false');
    }
});