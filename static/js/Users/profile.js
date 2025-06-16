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

    $('.history-coins-block').hide();
    $('.history-coins-label').click(function() {
        $('.history-coins-block').toggle();
    });

});