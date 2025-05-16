$(document).ready(function () {

    var successMessage = $("#jq-notification-success");
    var dangerMessage = $("#jq-notification-danger");

    $('#visits_inf').hide();
    $('#visits').click(function(){
        $('#visits_inf').toggle();
    });

    $('#guardianship_inf').hide()
    $('#guardianship').click(function(){
        $('#guardianship_inf').toggle();
    });

    $('#id_logout').click(function(e) {
        e.preventDefault();
        var token = '';
        function getCookie(cname) {
            var name = cname + "=";
            var ca = document.cookie.split(';');
            for(var i=0; i<ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1);
                if (c.indexOf(name) != -1) return c.substring(name.length,c.length);
            }
            return "";
        }
        $.ajax({
            method: "POST",
            url: "../api/auth/token/logout/",
            data: {csrfmiddlewaretoken: document.querySelector('[name=csrfmiddlewaretoken]').value},
            headers: {
                "Authorization": getCookie('Authorization')
            },
            success: function(data){
                console.log('ok');
                $.post('../logout/', {csrfmiddlewaretoken: document.querySelector('[name=csrfmiddlewaretoken]').value});
                localStorage.setItem('succsessMsgText', 'Вы вышли из своего аккаунта');
                localStorage.setItem('msg', 'true');
                setTimeout(function () {
                    console.log("Redirecting");
                    window.location.href = '../login/';
            }, 50);
            },
            error: function (data){
                console.log('err');
                console.log(data);
            },
        });
    });


    $('#user_forms').on('submit', function (event) {
        var phone = $('#id_phone').val();
        var cleanedPhone = phone.replace(/\D/g, '');
        $('#id_phone').val(cleanedPhone);
    });


    $("#ChangePassword").hide();
    $("#BtnChangePassword").click(function() {
        if ($("#ChangePassword").is(':hidden')){
            $("#ChangePassword").show();
            $('.my-container').animate({height: '660px', top: '51.7%'}, 500);
        }
        else{
            $("#ChangePassword").hide();
            $('.my-container').animate({height: '540px'}, 500);
        }
    });


    $('#user_forms').on('submit', function (event){
        event.preventDefault();
        var fields = $('#user_forms').serializeArray();
        var currentUrl = $(location).attr('href');
        var u = '';
        var method = '';
        var succsessMsgText = '';
        var inputs = {};
        if (currentUrl.indexOf("change") != -1){
            if (!($("#ChangePassword").is(':hidden'))){
                u = '../../api/auth/users/set_password/';
                succsessMsgText = `Пароль был изменен`;
                method = 'POST';
                $('#user_forms :input[name]').each(function() {
                    if (jQuery.inArray(this.name, ['current_password', 'new_password', 're_new_password']) !== -1){
                        console.log(this.name);
                        inputs[this.name] = $(this).val();
                    }
                });
            }
            else{
                u = '../../api/auth/my/profile/';
                succsessMsgText = `${fields[1].value}, данные профиля были измененны`;
                method = 'PUT';
                $('#user_forms :input[name]').each(function() {
                    if (jQuery.inArray(this.name, ['current_password', 'new_password', 're_new_password']) === -1){
                        inputs[this.name] = $(this).val();
                        if (this.name == 'birthday' & $(this).val() == ''){
                            inputs[this.name] = null;
                        }
                    }
                });
            }
        }
        $.ajax({
        data: JSON.stringify(inputs),
        type: method,
        url: u,
        contentType: 'application/json',
        processData: false,
        success: function(data){
            console.log('ok');
            localStorage.setItem('succsessMsgText', succsessMsgText);
            localStorage.setItem('msg', 'true');
            $("#user_forms")[0].reset();
            setTimeout(function () {
                console.log("Redirecting");
                window.location.href = '../';
            }, 50);
            $.each(fields,function(){
                if($(`#id_${this.name}`).hasClass('is-valid')){
                    $(`#id_${this.name}`).removeClass("is-valid");
                }
                if($(`#id_${this.name}`).hasClass('is-invalid')){
                    $(`#id_${this.name}`).removeClass("is-invalid");
                    $(`#id_${this.name}_feedback`).empty();
                }
            });
        },
        error: function (data){
            console.log('err');
            var response = data.responseJSON;
            $.each(fields,function(){
                if (response){
                    if (jQuery.inArray(this.name, ['new_password', 're_new_password']) !== -1){
                        if (inputs['new_password'] != inputs['re_new_password']){
                            response['re_new_password'] = 'Пароли не совпадают';
                            console.log(response);
                        }
                    }
                    if(this.name in response){
                        Object.entries(response).forEach(([key, value]) =>{
                            if(!$(`#id_${key}`).hasClass('is-invalid')){
                                ($(`#id_${key}`)).addClass("is-invalid");
                                ($(`#id_${key}_feedback`)).append(`${value}`);
                                if (!($("#ChangePassword").is(':hidden'))){
                                    ($(document)).mouseup( function(e){
                                        ($(`#id_${key}_feedback`)).hide();
                                        ($(`#id_${key}_feedback`)).append(`${value}`);
                                        if ($(`#id_${key}`).is(e.target)){
                                            ($(`#id_${key}_feedback`)).show();
                                            if (jQuery.type(value) === "array"){
                                                $("#SaveChangesbtn").hide();
                                            }
                                        }
                                        else{
                                            ($(`#id_${key}_feedback`)).hide();
                                            if (jQuery.type(value) === "array"){
                                                $("#SaveChangesbtn").show();
                                            }
                                        }
                                    });
                                }
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