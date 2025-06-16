$(document).ready(function () {

    $.ajax({
        url: '../api/auth/my/profile/',
        method: 'GET',
        dtaType: 'json',
        xhrFields: {
            withCredentials: true, // Отправка кук
        },
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': '{{ csrf_token }}',
        },
        success: function (data) {
            console.log('Data was get successfully!');

            //mainInf-cont
            $('div[name=username]').append(data.username);
            $('div[name=email]').append(data.email);
            $('div[name=phone]').append(data.phone);
            if (data.birthday == null){
                $('div[name=birthday]').append("Дата рождения не указана");
            }
            else{
                $('div[name=birthday]').append(data.birthday);
            }
            
            //visits-cont
            var bookings = data.booking
            var count_is_active = 0
            var count_isnt_active = 0

            if (bookings.length == 0) {
                $('#booking_doesnt_exist').removeClass('invisible');
            } 
            else {
                $('#booking_exists').removeClass('invisible');

                bookings.forEach(booking => {
                    if (!booking.is_inactive) {
                        count_is_active++
                        $('#append_is_active').append(`
                            <li class="list-img list-item txt-content row">
                                <div class="booking-container mx-2 pl-4 py-1 col-9">
                                    <div class="row">
                                        <div class="col-5">Дата:
                                            <span class="txt-headline mx-1 fs-7">${booking.date}</span>
                                        </div>
                                        <div class="col-7">Время:
                                            <span class="txt-headline mx-1 fs-7">${booking.time}</span>
                                        </div>
                                    </div>
                                    <div>Адрес:
                                        <span class="txt-headline mx-1 fs-7">${booking.address.city}, ${booking.address.street}, ${booking.address.house_number}</span>
                                    </div>
                                    <div class="row">
                                        <div class="col-6">Количество человек:
                                            <span class="txt-headline mx-1 fs-7">${booking.quantity}</span>
                                        </div>
                                        <div class="col-6">Статус оплаты:
                                            <span class="txt-headline mx-1 fs-7">${booking.is_paid}</span>
                                        </div>
                                    </div>
                                    <div>Дата оформления:
                                        <span class="txt-headline mx-1 fs-7">${booking.created_timestamp}</span>
                                    </div>
                                </div>
                                <div class="align-self-center col-2">
                                    <button id="${booking.id}" type="button" class="btn_modal btn btn-dark btn-block px-3 py-2" data-bs-toggle="modal"
                                            data-bs-target="#modal_del_booking">Отменить посещение</button>
                                </div>
                            </li>
                        `);
                    } 
                    else {
                        count_isnt_active++
                        $('#append_isnt_active').append(`
                            <li class='list-img list-item txt-content row'>
                                <div class='booking-container mx-2 pl-4 py-1 col-9'>
                                    <div class='row'>
                                        <div class='col-5'>Дата:<span class='txt-headline mx-1 fs-7'>${booking.date}</span></div>
                                        <div class='col-7'>Время:<span class='txt-headline mx-1 fs-7'>${booking.time}</span></div>
                                    </div>
                                    <div>
                                        Адресс:<span class='txt-headline mx-1 fs-7'>${booking.address.city}, ${booking.address.street}, ${booking.address.house_number}</span>
                                    </div>
                                    <div class='row'>
                                        <div class='col-6'>
                                            Количество человек:
                                            <span class='txt-headline mx-1 fs-7'>${booking.quantity}</span>
                                        </div>
                                        <div class='col-6'>
                                            Статус оплаты:
                                            <span class='txt-headline mx-1 fs-7'>${booking.is_paid}</span>
                                        </div>
                                    </div>
                                    <div>
                                        Дата оформления:
                                        <span class='txt-headline mx-1 fs-7'>${booking.created_timestamp}</span>
                                    </div>
                                </div>
                            </li>
                        `)
                    }
                });

                $('#modal_del_booking').on('show.bs.modal', function(data){

                    var id = null;
                    if ($('#is_active .btn_modal').is(':focus')) {
                        id = $('#is_active .btn_modal').attr('id') // Или нужное значение
                    }

                    $(`#${id}, #modal_cat_happy`).hide();
                    $(`#${id}, #modal_no`).mouseover(function(){
                        $(`#${id}, #modal_cat_sad`).hide();
                        $(`#${id}, #modal_cat_happy`).show();
                        $('.btn_modal').show();
                    });
                    $(`#${id}, #modal_no`).mouseout(function(){
                        $(`#${id}, #modal_cat_sad`).show();
                        $(`#${id}, #modal_cat_happy`).hide();
                        $('.btn_modal').show();
                    });

                    $('#modal_no').click(function(event) {
                        id = null;
                    });

                    $('.modal_yes').click(function(event) {
                        event.preventDefault();
                        succsessMsgText = 'Запись была удалена';
                        $.ajax({
                            url:`../../calendar/api/booking/${id}`,
                            type: 'DELETE',
                            success: function(response) {
                                localStorage.setItem('succsessMsgText', succsessMsgText);
                                localStorage.setItem('msg', 'true');
                                setTimeout(function () {
                                    location.reload(true);
                                }, 50);
                            },
                            error: function(response){
                                console.log('err -', response);
                            }                                
                        });
                    });

                });
            }

            if (count_is_active == 0) {
                $('div.booking-near').append(
                    `<p class="text-center txt-content mb-5 mt-2 fs-6">У вас нет ближайших записей 😿</p>`
                )
            }
            if (count_isnt_active == 0) {
                $('div.booking-history')
                    .append(`<p class="text-center txt-content mb-5 mt-2 fs-6">Здесь будет находится информация
            о ваших <span class="text-wavy">предыдущих посещениях</span></p>`)
            }

            //guardianship-cont
            var guardianships = data.guardianship;

            if (guardianships.length == 0) {
                $('#guardianship_doesnt_exist').removeClass('invisible');
            } 
            else {
                $('#guardianship_exists').removeClass('invisible');

                guardianships.forEach(guardianship => {
                    $('#append_cats').append(`
                        <li class="list-img list-item txt-content row">
                            <div class="guardian-container mx-2 pl-4 py-1 col-8">
                                <div class="row">
                                    <div class="col-5">Кличка:
                                        <a class="txt-headline mx-1" href="{% url 'cats:our_cats' %}">${guardianship.cat_name}</a>
                                    </div>
                                    <div class="col-7">Сумма подписки:
                                        <a class="txt-headline mx-1 fs-7">${guardianship.amount_of_money}</a><span>₽</span>
                                    </div>
                                </div>
                                <div>Дата оформления подписки:
                                    <span class="txt-headline mx-1 fs-7">${guardianship.created_timestamp}</span>
                                </div>
                            </div>
                            <div class="align-self-center col-3">
                                <button id="${guardianship.id}" name="sub" class="btn_modal btn_sub btn btn-dark btn-block" type="button" data-bs-toggle="modal" data-bs-target="#modal_del_sub">
                                    Отменить подписку</button>
                            </div>
                        </li>
                    `)
                    console.log(guardianship.id)
                });

                $('#modal_del_sub').on('show.bs.modal', function(data){

                    var id = null;
                    if ($('#append_cats .btn_modal').is(':focus')) {
                        id = $('#append_cats .btn_modal').attr('id') // Или нужное значение
                    }

                    $(`#${id}, #modal_cat_happy`).hide();
                    $(`#${id}, #modal_no`).mouseover(function(){
                        $(`#${id}, #modal_cat_sad`).hide();
                        $(`#${id}, #modal_cat_happy`).show();
                        $('.btn_modal').show();
                    });
                    $(`#${id}, #modal_no`).mouseout(function(){
                        $(`#${id}, #modal_cat_sad`).show();
                        $(`#${id}, #modal_cat_happy`).hide();
                        $('.btn_modal').show();
                    });

                    $('#modal_no').click(function(event) {
                        id = null;
                    });

                    $('.modal_yes').click(function(event) {
                        event.preventDefault();
                        succsessMsgText = 'Подписка отменена';
                        $.ajax({
                            url:`../../payment/del-sub/`,
                            type: 'POST',
                            data: {
                                csrfmiddlewaretoken: document.querySelector('[name=csrfmiddlewaretoken]').value,
                                'guardian_id': id
                            },
                            success: function(response) {
                                console.log(response.data);
                                localStorage.setItem('succsessMsgText', succsessMsgText);
                                localStorage.setItem('msg', 'true');
                                setTimeout(function () {
                                    location.reload(true);
                                }, 50);
                            },
                            error: function(response){
                                console.log('err -', response);
                            }
                        });
                    });

                });
            }

            //bonuses-cont
            var coins = data.coins
            var histories = coins.histories

            $('div[name=coins_count]').append(coins.count);

            histories.forEach(history => {
                $('div[name=history-coins]').append(`
                    <div class="history-coins-container col-12 py-4 mt-4">
                        <div class="d-flex align-items-center justify-content-center">
                            <div class="col-4 ps-4">
                                <h5 class="txt-headline txt-select ">Дата:</h5>
                                <p>${history.created_timestamp}</p>
                            </div>
                            <div class="col-5 mx-2">
                                <h5 class="txt-headline txt-select">Описание:</h5>
                                <p>${history.description}</p>
                            </div>
                            <div class="col-3">
                                <h5 class="txt-headline txt-select">Мяукоины:</h5>
                                ${history.count}
                            </div>
                        </div>
                    </div>
                `)
            });
            
        },
        error: function (data) {
            console.error('Failed to get data:', data);
        }
    });

});