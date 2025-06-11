$(document).ready(function () {
	$.ajax({
		url: 'api/information/',
		type: 'GET',
		dataType: 'json',
		xhrFields: {
			withCredentials: true, // Отправка кук
		},
		headers: {
			'X-Requested-With': 'XMLHttpRequest',
			'X-CSRFToken': '{{ csrf_token }}',
		},
		success: function (data) {
            console.log(data[0]);
            $('span[name=count_of_cats]').append(
							`${data[0].count_of_cats} котиков`
						)
			$('span[name=working_hours]').append(data[0].working_hours)
            if (data[0].duration_of_the_visit == 1){
                $('span[name=duration_of_the_visit]').append(`${data[0].duration_of_the_visit} час`)
            }
            else{
                $('span[name=duration_of_the_visit]').append(`${data[0].duration_of_the_visit} часа`)
            }
            $('span[name=cost]').append(`${data[0].cost} ₽`)
            $('span[name=phone]').append(data[0].phone)
            $('span[name=address]').append(
							`${data[0].address.city}, ${data[0].address.street}, ${data[0].address.house_number}`
						)
		},
		error: function (data) {
			console.log('err')
		},
	})
})
