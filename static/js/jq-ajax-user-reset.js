$(document).ready(function () {

    var successMessage = $("#jq-notification-success");
    var dangerMessage = $("#jq-notification-danger");


    $('#user_forms_reset').on('submit', function (event){
        event.preventDefault();
        var fields = $('#user_forms_reset').serializeArray();
        var $data = {};
        $('#user_forms_reset :input[name]').each(function() {
            $data[this.name] = $(this).val();
        });
        var successMsgText = '';
        var u = '';
        var currentUrl = $(location).attr('href');
        if (currentUrl.indexOf("email") != -1){
            u = '../../api/auth/users/reset_password/';
            successMsgText = 'Письмо было отправлено на почту';
        }
        if (currentUrl.indexOf("password") != -1){
            u = '../../../../../api/auth/users/reset_password_confirm/';
            successMsgText = 'Пароль изменен';
            var form = $(this);
            var formUrl=form.attr('action');
            $data["uid"] = formUrl.split('/')[5];
            $data["token"] = formUrl.split('/')[6];
        }
        console.log($data);
        $.ajax({
            data: JSON.stringify($data),
            type: 'POST',
            url: u,
            contentType: 'application/json',
            processData: false,
            success: function(data){
                console.log('ok');
                $("#id_feedback").hide();
                $("#user_forms_reset")[0].reset();
                $.each(fields,function(){
                    if($(`#id_${this.name}`).hasClass('is-valid')){
                        $(`#id_${this.name}`).removeClass("is-valid");
                    }
                    if($(`#id_${this.name}`).hasClass('is-invalid')){
                        $(`#id_${this.name}`).removeClass("is-invalid");
                        $(`#id_${this.name}_feedback`).empty();
                    }
                });
                if (currentUrl.indexOf("password") != -1){
                    localStorage.setItem('successMsgText', successMsgText);
                    localStorage.setItem('msg', 'true');
                    setTimeout(function () {
                        console.log("Redirecting");
                        window.location.href = '../login/';
                    }, 50);
                }
                else{
                    successMessage.html(successMsgText);
                    successMessage.fadeIn(400);
                    setTimeout(function () {
                        successMessage.fadeOut(400);
                    }, 4000);
                }
            },
            error: function (data){
                var response = data.responseJSON;
                $("#id_feedback").show();
                if ($data['new_password'] != $data['re_new_password']){
                    response['re_new_password'] = 'Пароли не совпадают';
                }
                console.log(response);
                $.each(fields,function(){
                    if (response){
                        if(this.name in response){
                            Object.entries(response).forEach(([key, value]) =>{
                                if(!$(`#id_${key}`).hasClass('is-invalid')){
                                    ($(`#id_${key}`)).addClass("is-invalid");
                                    ($(`#id_${key}_feedback`)).append(`${value}`);
                                }
                            });
                        }
                        else{
                            if($(`#id_${this.name}`).hasClass('is-invalid')){
                                ($(`#id_${this.name}`)).removeClass("is-invalid");
                                ($(`#id_${this.name}`)).addClass("is-valid");
                                ($(`#id_${this.name}_feedback`)).empty();
                            }
                            if(!$(`#id_${this.name}`).hasClass('is-valid')){
                                ($(`#id_${this.name}`)).addClass("is-valid");
                            }
                        }
                    }
                    dangerMessage.html('Проверьте правильность заполнения полей');
                    dangerMessage.fadeIn(400);
                    setTimeout(function () {
                        dangerMessage.fadeOut(400);
                    }, 4000);
                });
            }
        });
        return false;
    });

});