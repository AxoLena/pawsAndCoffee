$(document).ready(function () {

    async function copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text)
            console.log('Текст скопирован в буфер обмена')
            return true
        } catch (err) {
            console.error('Ошибка копирования: ', err)
            return false
        }
    }
      

    $('.copy-btn').click(function(e){
        var copy_inf = $(this).closest('p').children('span:first');
        copyToClipboard(copy_inf.text())
        // var $temp = $("<input>");
        // $("body").append($temp);
        // $temp.val(copy_inf.text()).select();
	    // document.execCommand("copy");
	    // $temp.remove();
        copy_inf.addClass('select-active');
        setTimeout(function() {
            copy_inf.removeClass('select-active');
        }, 300);
    });

});