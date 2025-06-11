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


});