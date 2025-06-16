$(document).ready(function () {
    $.ajax({
        url: '../../bonus/api/coupon/list/',
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

            data.forEach(coupon => {
                $('div[name=coupons]').append(`
                    <div class="card-discounts css-${ coupon.code } txt-content">
                        <div class="img">
                            <p>${coupon.code}</p>
                            <p>${coupon.description}</p>
                            <p>${coupon.discount}%</p>
                        </div>
                    </div>
                `);
            });

        },
        error: function (data) {
            console.error('Failed to get data:', data)
        },
    });
});