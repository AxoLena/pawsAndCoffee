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

    $('.history-coins-block').hide();
    $('.history-coins-label').click(function() {
        $('.history-coins-block').toggle();
    });

});