$(document).ready(function () {

    var successMessage = $("#jq-notification-success");
    var dangerMessage = $("#jq-notification-danger");

    $("#AnotherPets").hide();
    $("input[name='has_pet']").change(function() {
        if ($("input[name='has_pet']").is(':checked')){
            $("#AnotherPets").show();
        } else {
            $("#AnotherPets").hide();
        }
    });

    $('#cat_forms').on('submit', function (event) {
        var phone = $('#id_phone').val();
        var cleanedPhone = phone.replace(/\D/g, '');
        $('#id_phone').val(cleanedPhone);
    });

    $('#cat_forms').on('submit', function (event){
        event.preventDefault();
        var formData = new FormData(this);
        var currentUrl = $(location).attr('href');
        var u = '';
        if (currentUrl.indexOf("adopt") != -1){
            u = '../api/adopt/';
        }
        if (currentUrl.indexOf("give") != -1){
            u = '../api/give/';
        }
        if (currentUrl.indexOf("guardianship") != -1){
            u = '../api/guardianship/';
        }
        $.ajax({
            data: formData,
            type: this.method,
            url: u,
            contentType: false,
            processData: false,
            success: function(data){
                console.log('ok');
                var valid = JSON.parse(data.valid_data);
                if (data.result == 'error'){
                    var err = JSON.parse(data.errors);
                    Object.entries(err).forEach(([key, value]) => {
                        if(!$(`#id_${key}`).hasClass('is-invalid')){
                            $(`#id_${key}`).addClass("is-invalid");
                            $(`#id_${key}_feedback`).append(`${value}`);
                        }
                    });
                    valid.forEach(function(item){
                        if($(`#id_${item}`).hasClass('is-invalid')){
                            $(`#id_${item}`).removeClass("is-invalid");
                            $(`#id_${item}_feedback`).empty();
                        }
                        if(!$(`#id_${item}`).hasClass('is-valid')){
                            $(`#id_${item}`).addClass("is-valid");
                        }
                    });
                    dangerMessage.html(data.message);
                    dangerMessage.fadeIn(400);
                    setTimeout(function () {
                        dangerMessage.fadeOut(400);
                    }, 4000);
                }
                else{
                    successMessage.html(data.message);
                    successMessage.fadeIn(400);
                    setTimeout(function () {
                        successMessage.fadeOut(400);
                    }, 4000);
                    $("#cat_forms")[0].reset();
                    valid.forEach(function(item){
                        if($(`#id_${item}`).hasClass('is-valid')){
                            $(`#id_${item}`).removeClass("is-valid");
                        }
                        if($(`#id_${item}`).hasClass('is-invalid')){
                            $(`#id_${item}`).removeClass("is-invalid");
                            $(`#id_${item}_feedback`).empty();
                        }
                    });
                    if (currentUrl.indexOf("guardianship") != -1){
                        setTimeout(function () {
                            console.log("Redirecting");
                            window.location.href = '../../payment/guardianship/';
                        }, 1000);
                    }
                }
            },
            error: function (data){
                alert('На сервере произошла ошибка!');
                console.log('err');
            }
        });
        return false;
    });

});