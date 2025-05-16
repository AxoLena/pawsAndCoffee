$(document).ready(function () {

    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth();

    const day = document.querySelector(".calendar-dates");
    const currdate = document.querySelector(".calendar-current-date");

    const months = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"];

    const calendar = () => {
        var firstdayweek = new Date(year, month, 0).getDay();
        var lastdate = new Date(year, month + 1, 0).getDate();
        var lit = "";

        if (firstdayweek == 0){
            for (var m = 0; m < 6; m++) {
                lit += `<li class="invisible"></li>`;
            }
        }

        for (var i = 0; i != firstdayweek; i++){
            lit += `<li class="invisible"></li>`;
        }

        for (var i = 1; i <= lastdate; i++) {
            var isToday = i === date.getDate() && month === new Date().getMonth() && year === new Date().getFullYear() ? "active"
                : i < date.getDate() && month === new Date().getMonth() && year === new Date().getFullYear() ? "inactive"
                : "none";
            lit += `<li class="${isToday}" id="day_${isToday}">${i}</li>`;
        }

        currdate.innerText = `${months[month]} ${year}`;
        day.innerHTML = lit;
    }
    calendar()

    var date = null
    var time = null
    var address = null

    var days_click = document.querySelectorAll('#day_none, #day_active');
    var last_select_day = null;
    var last_el = null;
    var select_time = null;
    var dt = new Date();
    days_click.forEach( el => {
        el.addEventListener('click', () =>{
            var select_day = el.textContent;
            console.log('ok');
            if ($(`#time_${select_day}`).length != 0) {
                $(`#choice_times`).children().remove();
                $('#no_selected').show();
                el.classList.remove('select');
            }
            else {
                if ($(`#time_${last_select_day}`).length != 0){
                    $(`#choice_times`).children().remove();
                    last_el.classList.remove('select');
                }
                el.classList.add('select');
                last_select_day = select_day;
                last_el = el;
                $.ajax({
                    url: 'api/schedule/day/',
                    method: 'get',
                    dataType: 'json',
                    data: {'day': select_day},
                    success: function(response){
                        $('#no_selected').hide();
                        if(response.length > 0){
                             for(var i=0; i<response.length;i++){
                                 if(select_day == Number(dt.getDate())){
                                     if(Number(response[i].time.split(":")[0]) > dt.getHours()){
                                        $('#choice_times').append(`
                                        <div class='my-4 d-flex justify-content-center align-items-center col' id='time_${select_day}'>
                                            <div class="time-item py-3 px-5 d-flex flex-column align-items-center txt-content">
                                                <p>Время: <span class="txt-headline fs-5">${response[i].time}</span></p>
                                                <p>Оставшихся мест: <span class="txt-headline fs-5">${response[i].number_of_places}</span></p>
                                                <button type="button" id="${i}" class="btn_model btn btn-dark btn-block" data-bs-toggle="modal"
                                                data-bs-target="#modal_booking">Записаться</button>
                                            </div>
                                        </div>`);
                                     }
                                     else{
                                         if($(`#choice_times`).children().length == 0){
                                             $('#choice_times').append(`
                                            <div class='py-2 fs-5 col-12 text-center' id='time_${select_day}'>
                                                <div class=''>К сожалению, на этот день уже нет свободных окошек :(</div>
                                                <div class="img-sad-cat mb-3"></div>
                                            </div>`);
                                         }
                                     }
                                 }
                                 else{
                                     $('#choice_times').append(`
                                        <div class='my-4 d-flex justify-content-center align-items-center col' id='time_${select_day}'>
                                            <div class="time-item py-3 px-5 d-flex flex-column align-items-center txt-content">
                                                <p>Время: <span class="txt-headline fs-5">${response[i].time}</span></p>
                                                <p>Оставшихся мест: <span class="txt-headline fs-5">${response[i].number_of_places}</span></p>
                                                <button type="button" id="${i}" class="btn_model btn btn-dark btn-block" data-bs-toggle="modal"
                                                data-bs-target="#modal_booking">Записаться</button>
                                            </div>
                                        </div>`);
                                 }
                             }
                            $('.btn_model').click(function(event) {
                                event.preventDefault();
                                $.ajax({
                                    url: 'api/schedule/time/',
                                    method: 'get',
                                    dataType: 'json',
                                    data: {'day': select_day, 'time': this.id},
                                    success: function(resp){
                                        date = resp[0].date
                                        time = resp[0].time
                                        address = resp[0].address
                                        $('#modal_inf_booking').append(
                                            `<div class="mt-3 d-flex">
                                                <div class="mb-3 px-2 col-6">
                                                    <label class="form-label mx-4">Дата</label>
                                                    <div class="form-control">${date}</div>
                                                </div>
                                                <div class="mb-3 px-2 col-6">
                                                    <label class="form-label mx-4">Время</label>
                                                    <div class="form-control">${time}</div>
                                                </div>
                                            </div>
                                            <div class="mb-3 px-2">
                                                <label class="form-label mx-4">Адресс</label>
                                                <div class="form-control">${address.city}, ${address.street}, ${address.house_number}</div>
                                            </div>`
                                        );
                                    }
                                });
                            });
                            $('.btn-close').click(function(){
                                $('#modal_inf_booking').children().remove();
                            });
                        }
                        else{
                            $('#choice_times').append(`
                                <div class='py-2 fs-5 col-12 text-center' id='time_${select_day}'>
                                    <div class=''>К сожалению, на этот день еще нет расписания</div>
                                    <div class="img-sad-cat mb-3"></div>
                                </div>`);
                        }
                    },
                    error: function (response){
                        alter('На сервере произошла ошибка!');
                        console.log('err');
                    }
                });
            }
        });
    });


    var user_id = null;
    if ($('.pay_coins').attr('id') !== undefined ){
        user_id = $('.pay_coins').attr('id').split('_')[0];
        $.ajax({
            url: `../user/api/auth/profile/inf/${user_id}/`,
            method: 'get',
            dataType: 'json',
            success: function(resp){
                var coins = resp.coins.count;
                $('#inf_user_coins').append(
                    `<div class="px-3 coins">${coins}</div>`
                );
                $('#id_coins').attr({
                    max:coins,
                    min:0,
                    value:0,
                });
            },
            error: function(resp){
                console.log('error - ', resp);
            }
        });
    }

    $('#coin_form').on('input', 'input', function() {
        var val_coin = $(this).val();
        $('#minus_coin').html(`-${val_coin}₽`);
    });

    $('#quantity_form').on('input', 'input', function() {
        var val_coin = $(this).val();
        $('#multiply_quantity').html(`X${val_coin}`);
    });

    $('.pay_coins').hide();
    $('#pay_coins_submit').on('click', function(event){
        $('.pay_coins').toggle();
    });

    $('#modal_booking_form').on('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        var fields = $('#modal_booking_form').serializeArray();
        formData.append('address_id', address.id);
        var date_arr = date.split('-');
        var format_date = date_arr[2] + '-' + date_arr[1] + '-' + date_arr[0];
        formData.append('date', format_date);
        formData.append('time', time);
        var cost = 200;
        var coins = Number(formData.get('coins'));
        if ($('#id_coins').val() != 0){
            var coin_id = $('.pay_coins').attr('id').split('_')[1];
            formData.append('bonuses', coins);
        }
        else{
            formData.append('bonuses', 0);
        }
        if ($('#id_code').val() != ''){
            $.ajax({
                url: `../bonus/api/coupon/compare/`,
                type: 'POST',
                processData: false,
                contentType: false,
                data: formData,
                success: function(response){
                    var data = response.responseJSON;
                    formData.append('coupon', response.code);
                    $.ajax({
                        data: formData,
                        url: 'api/booking/',
                        method: 'post',
                        contentType: false,
                        processData: false,
                        success: function(response){
                            if ($('#id_coins').val() != 0){
                                if(!$(`#id_coins, #id_code`).hasClass('is-invalid')){
                                    ($(`#id_coins, #id_code`)).addClass("is-invalid");
                                    ($(`#id_coins_feedback, #id_code_feedback`)).append(`
                                    Нельзя использовать промокод и бонусы вместе! выберите что-то одно`);
                                }
                            }
                            else{
                                setTimeout(function () {
                                    console.log("Redirecting");
                                    window.location.href = '../payment/booking/';
                                }, 1000);
                            }
                        },
                        error: function(data){
                            var response = data.responseJSON;
                            console.log('err - ', response);
                            $("#id_feedback").show();
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
                            });
                        }
                    });
                },
                error: function(response){
                    var data = response.responseJSON;
                    console.log('err - ', data);
                    $.each(fields,function(){
                        if (data){
                            if(this.name in data){
                                Object.entries(data).forEach(([key, value]) =>{
                                    if(!$(`#id_${key}`).hasClass('is-invalid')){
                                        ($(`#id_${key}`)).addClass("is-invalid");
                                        ($(`#id_${key}_feedback`)).append(`${value}`);
                                    }
                                    else{
                                        ($(`#id_${this.name}_feedback`)).empty();
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
                    });
                }
            });
        }
        $.ajax({
            data: formData,
            url: 'api/booking/',
            method: 'post',
            contentType: false,
            processData: false,
            success: function(response){
                if ($('#id_coins').val() != 0){
                    var coin_id = $('.pay_coins').attr('id').split('_')[1];
                    $.ajax({
                        url: `../bonus/api/bonus/update/${coin_id}/`,
                        type: 'PATCH',
                        processData: false,
                        contentType: 'application/json',
                        data: JSON.stringify({
                            coins: coins,
                            Authorization: $.cookie('Authorization'),
                        }),
                        success: function(response){
                            console.log(response);
                        },
                        error: function(response){
                            alter('На сервере произошла ошибка!');
                            console.log('err - ', respons);
                        }
                    });
                }
                setTimeout(function () {
                    console.log("Redirecting");
                    window.location.href = '../payment/booking/';
                }, 1000);
            },
            error: function(data){
                var response = data.responseJSON;
                console.log('err - ', response);
                $("#id_feedback").show();
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
                });
            }
        });
    });

});