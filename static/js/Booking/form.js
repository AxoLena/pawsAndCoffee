$(document).ready(function () {

		if ($('.pay_coins').attr('id') !== undefined) {
			$.ajax({
				url: `../user/api/auth/my/profile/`,
				method: 'get',
				dataType: 'json',
				success: function (resp) {
					var coins = resp.coins.count
					$('#inf_user_coins').append(`<div class="px-3 coins">${coins}</div>`)
					$('#id_coins').attr({
						max: coins,
						min: 0,
						value: 0,
					})
				},
				error: function (resp) {
					console.log('error - ', resp)
				},
			})
		}

		$('#coin_form').on('input', 'input', function () {
			var val_coin = $(this).val()
			$('#minus_coin').html(`-${val_coin}₽`)
		})

		$('#quantity_form').on('input', 'input', function () {
			var val_coin = $(this).val()
			$('#multiply_quantity').html(`X${val_coin}`)
		})

		$('.pay_coins').hide()
		$('#pay_coins_submit').on('click', function (event) {
			$('.pay_coins').toggle()
		})

		$('#modal_booking_form').on('submit', function (event) {
			event.preventDefault()
			var formData = new FormData(this)
			var fields = $('#modal_booking_form').serializeArray()
			formData.append('address_id', address.id)
			var date_arr = date.split('-')
			var format_date = date_arr[2] + '-' + date_arr[1] + '-' + date_arr[0]
			formData.append('date', format_date)
			formData.append('time', time)
			var cost = 200
			var coins = Number(formData.get('coins'))
			if ($('#id_coins').val() != 0) {
				var coin_id = $('.pay_coins').attr('id').split('_')[1]
				formData.append('bonuses', coins)
			} else {
				formData.append('bonuses', 0)
			}
			if ($('#id_code').val() != '') {
				$.ajax({
					url: `../bonus/api/coupon/compare/`,
					type: 'POST',
					processData: false,
					contentType: false,
					data: formData,
					success: function (response) {
						var data = response.responseJSON
						formData.append('coupon', response.code)
						$.ajax({
							data: formData,
							url: 'api/booking/',
							method: 'post',
							contentType: false,
							processData: false,
							success: function (response) {
								if ($('#id_coins').val() != 0) {
									if (!$(`#id_coins, #id_code`).hasClass('is-invalid')) {
										$(`#id_coins, #id_code`).addClass('is-invalid')
										$(`#id_coins_feedback, #id_code_feedback`).append(`
                                    Нельзя использовать промокод и бонусы вместе! выберите что-то одно`)
									}
								} else {
									setTimeout(function () {
										console.log('Redirecting')
										window.location.href = '../payment/booking/'
									}, 1000)
								}
							},
							error: function (data) {
								var response = data.responseJSON
								console.log('err - ', response)
								$('#id_feedback').show()
								$.each(fields, function () {
									if (response) {
										if (this.name in response) {
											Object.entries(response).forEach(([key, value]) => {
												if (!$(`#id_${key}`).hasClass('is-invalid')) {
													$(`#id_${key}`).addClass('is-invalid')
													$(`#id_${key}_feedback`).append(`${value}`)
												}
											})
										} else {
											if ($(`#id_${this.name}`).hasClass('is-invalid')) {
												$(`#id_${this.name}`).removeClass('is-invalid')
												$(`#id_${this.name}`).addClass('is-valid')
												$(`#id_${this.name}_feedback`).empty()
											}
											if (!$(`#id_${this.name}`).hasClass('is-valid')) {
												$(`#id_${this.name}`).addClass('is-valid')
											}
										}
									}
								})
							},
						})
					},
					error: function (response) {
						var data = response.responseJSON
						console.log('err - ', data)
						$.each(fields, function () {
							if (data) {
								if (this.name in data) {
									Object.entries(data).forEach(([key, value]) => {
										if (!$(`#id_${key}`).hasClass('is-invalid')) {
											$(`#id_${key}`).addClass('is-invalid')
											$(`#id_${key}_feedback`).append(`${value}`)
										} else {
											$(`#id_${this.name}_feedback`).empty()
											$(`#id_${key}_feedback`).append(`${value}`)
										}
									})
								} else {
									if ($(`#id_${this.name}`).hasClass('is-invalid')) {
										$(`#id_${this.name}`).removeClass('is-invalid')
										$(`#id_${this.name}`).addClass('is-valid')
										$(`#id_${this.name}_feedback`).empty()
									}
									if (!$(`#id_${this.name}`).hasClass('is-valid')) {
										$(`#id_${this.name}`).addClass('is-valid')
									}
								}
							}
						})
					},
				})
			}
			$.ajax({
				data: formData,
				url: 'api/booking/',
				method: 'post',
				contentType: false,
				processData: false,
				success: function (response) {
					if ($('#id_coins').val() != 0) {
						var coin_id = $('.pay_coins').attr('id').split('_')[1]
						$.ajax({
							url: `../bonus/api/bonus/update/${coin_id}/`,
							type: 'PATCH',
							processData: false,
							contentType: 'application/json',
							data: JSON.stringify({
								coins: coins,
								Authorization: $.cookie('Authorization'),
							}),
							success: function (response) {
								console.log(response)
							},
							error: function (response) {
								alter('На сервере произошла ошибка!')
								console.log('err - ', respons)
							},
						})
					}
					setTimeout(function () {
						console.log('Redirecting')
						window.location.href = '../payment/booking/'
					}, 1000)
				},
				error: function (data) {
					var response = data.responseJSON
					console.log('err - ', response)
					$('#id_feedback').show()
					$.each(fields, function () {
						if (response) {
							if (this.name in response) {
								Object.entries(response).forEach(([key, value]) => {
									if (!$(`#id_${key}`).hasClass('is-invalid')) {
										$(`#id_${key}`).addClass('is-invalid')
										$(`#id_${key}_feedback`).append(`${value}`)
									}
								})
							} else {
								if ($(`#id_${this.name}`).hasClass('is-invalid')) {
									$(`#id_${this.name}`).removeClass('is-invalid')
									$(`#id_${this.name}`).addClass('is-valid')
									$(`#id_${this.name}_feedback`).empty()
								}
								if (!$(`#id_${this.name}`).hasClass('is-valid')) {
									$(`#id_${this.name}`).addClass('is-valid')
								}
							}
						}
					})
				},
			})
		})

});