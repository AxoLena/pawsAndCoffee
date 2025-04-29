$(document).ready(function () {

    $('.tabs .tab').click(function(){
        if ($(this).hasClass('mainInf')) {
            $('.tabs .tab').removeClass('active');
            $(this).addClass('active');
            $('.cont').hide();
            $('.mainInf-cont').show();
        }
        if ($(this).hasClass('visits')) {
            $('.tabs .tab').removeClass('active');
            $(this).addClass('active');
            $('.cont').hide();
            $('.visits-cont').show();
        }
        if ($(this).hasClass('guardianship')) {
            $('.tabs .tab').removeClass('active');
            $(this).addClass('active');
            $('.cont').hide();
            $('.guardianship-cont').show();
        }
        if ($(this).hasClass('bonuses')) {
            $('.tabs .tab').removeClass('active');
            $(this).addClass('active');
            $('.cont').hide();
            $('.bonuses-cont').show();
        }
    });

    if ($('ul.booking-near').children().length <= 0){
        $('div.booking-near').append(`<p class="text-center txt-content mb-5 mt-2 fs-6">У вас нет ближайших записей 😿</p>`);
    }

    if ($('ul.booking-history').children().length <= 0){
        $('div.booking-history').append(`<p class="text-center txt-content mb-5 mt-2 fs-6">Здесь будет находится информация
        о ваших <span class="text-wavy">предыдущих посещениях</span></p>`);
    }

    var id = null;

    $('.btn_modal').click(function() {
        id = this.id;
        console.log(id);
    });

    $('.history-coins-block').hide();
    $('.history-coins-label').click(function() {
        $('.history-coins-block').toggle();
    });


    $('#modal_del_booking, #modal_del_sub').on('show.bs.modal', function(data){
        var modal_id = $(this).attr('id');

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

        if (modal_id == "modal_del_booking"){
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
                return false;
            });
        }
        else {
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
                return false;
            });
        }

    });

});