$(document).ready(function () {

    var successMessage = $("#jq-notification-success");
    var dangerMessage = $("#jq-notification-danger");


    $('.tabs .tab').click(function(){
        if ($(this).hasClass('signin')) {
            $('.tabs .tab').removeClass('active');
            $(this).addClass('active');
            $('.cont').hide();
            $('.signin-cont').show();
            $('.my-container').animate({width: '850px'}, 500);
        }
        if ($(this).hasClass('signup')) {
            $('.tabs .tab').removeClass('active');
            $(this).addClass('active');
            $('.cont').hide();
            $('.signup-cont').show();
            $('.my-container').animate({width: '970px'}, 500);
        }
    });


    $('#user_forms').on('submit', function (event) {
        var phone = $('#id_phone').val();
        var cleanedPhone = phone.replace(/\D/g, '');
        $('#id_phone').val(cleanedPhone);
    });


    $("#id_feedback").hide();
    $('#user_forms_login').on('submit', function (event){
        event.preventDefault();
        var fields = $('#user_forms_login').serializeArray();
        var formData = new FormData(this);
        var succsessMsgText = `${fields[1].value}, с возвращением!`;
        $.ajax({
            data: formData,
            type: this.method,
            url: '../api/auth/token/login/',
            contentType: false,
            processData: false,
            success: function(data){
                console.log('ok');
                var token = data['auth_token'];
                $("#id_feedback").hide();
                $("#user_forms_login")[0].reset();
                $.each(fields,function(){
                    if($(`#user_forms_login #id_${this.name}`).hasClass('is-valid')){
                        $(`#user_forms_login #id_${this.name}`).removeClass("is-valid");
                    }
                    if($(`#user_forms_login #id_${this.name}`).hasClass('is-invalid')){
                        $(`#user_forms_login #id_${this.name}`).removeClass("is-invalid");
                        $(`#user_forms_login #id_${this.name}_feedback`).empty();
                    }
                });
                $.post('../login/', {
                        'auth-token': token,
                        'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
                });
                localStorage.setItem('succsessMsgText', succsessMsgText);
                localStorage.setItem('msg', 'true');
                setTimeout(function () {
                    console.log("Redirecting");
                    window.location.href = '../update/';
                }, 50);
            },
            error: function (data){
                var response = data.responseJSON;
                $("#id_feedback").show();
                $.each(fields,function(){
                    if (response){
                        if(this.name in response){
                            Object.entries(response).forEach(([key, value]) =>{
                                if(!$(`#user_forms_login #id_${key}`).hasClass('is-invalid')){
                                    $(`#user_forms_login #id_${key}`).addClass("is-invalid");
                                    $(`#user_forms_login #id_${key}_feedback`).append(`${value}`);
                                }
                            });
                        }
                        else{
                            if(!$(`#user_forms_login #id_${this.name}`).hasClass('is-invalid')){
                                $(`#user_forms_login #id_${this.name}`).addClass("is-invalid");
                            }
                            $("#user_forms_login #id_password").val('');
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


    $('#user_forms').on('submit', function (event){
        event.preventDefault();
        var fields = $('#user_forms').serializeArray();
        var formData = new FormData(this);
        var currentUrl = $(location).attr('href');
        var succsessMsgText = `${fields[1].value}, вы были успешно зарегистрированы`;
        $.ajax({
            data: formData,
            type: 'POST',
            url: '../api/auth/users/',
            contentType: false,
            processData: false,
            success: function(data){
                console.log('ok');
                successMessage.html(succsessMsgText);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 4000);
                $("#user_forms")[0].reset();
                $.each(fields,function(){
                    if($(`#user_forms #id_${this.name}`).hasClass('is-valid')){
                        $(`#user_forms #id_${this.name}`).removeClass("is-valid");
                    }
                    if($(`#user_forms #id_${this.name}`).hasClass('is-invalid')){
                        $(`#user_forms #id_${this.name}`).removeClass("is-invalid");
                        $(`#user_forms #id_${this.name}_feedback`).empty();
                    }
                });
            },
            error: function (data){
                var response = data.responseJSON;
                console.log('err - ', data);
                console.log(fields);
                $.each(fields,function(){
                    if (response){
                        if(this.name in response){
                            Object.entries(response).forEach(([key, value]) =>{
                                if(!$(`#user_forms #id_${key}`).hasClass('is-invalid')){
                                    ($(`#user_forms #id_${key}`)).addClass("is-invalid");
                                    ($(`#user_forms #id_${key}_feedback`)).hide();
                                    ($(`#user_forms #id_${key}_feedback`)).append(`${value}`);
                                    ($(document)).mouseup( function(e){
                                        if ($(`#user_forms #id_${key}`).is(e.target)){
                                            ($(`#user_forms #id_${key}_feedback`)).show();
                                        }
                                        else{
                                            ($(`#user_forms #id_${key}_feedback`)).hide();
                                        }
                                    });
                                }
                            });
                        }
                        else{
                            if($(`#user_forms #id_${this.name}`).hasClass('is-invalid')){
                                ($(`#user_forms #id_${this.name}`)).removeClass("is-invalid");
                                ($(`#user_forms #id_${this.name}`)).addClass("is-valid");
                                ($(`#user_forms #id_${this.name}_feedback`)).empty();
                            }
                            if(!$(`#user_forms #id_${this.name}`).hasClass('is-valid')){
                                ($(`#user_forms #id_${this.name}`)).addClass("is-valid");
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