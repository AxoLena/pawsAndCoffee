document.addEventListener('DOMContentLoaded', async () => {
	try {
		const response = await fetch('cats/api/cats/')
		const cats = await response.json()
		
		const indicatorsContainer = document.getElementById('carousel-indicators')
		const carouselInner = document.getElementById('carousel-inner')

		indicatorsContainer.innerHTML = ''
		carouselInner.innerHTML = ''

		cats.forEach((cat, index) => {
			const button = document.createElement('button')
			button.type = 'button'
			button.setAttribute('data-bs-target', '#carouselExampleCaptions')
			button.setAttribute('data-bs-slide-to', index)
			button.setAttribute('aria-label', `Slide ${index}`)

			if (index === 0) {
				button.classList.add('active')
				button.setAttribute('aria-current', 'true')
			}

			indicatorsContainer.appendChild(button)
		})

		cats.forEach((cat, index) => {
			const slide = document.createElement('div')
			slide.classList.add('carousel-item')
			if (index === 0) slide.classList.add('active')

			slide.innerHTML = `
                <div class="d-flex justify-content-center align-items-center">
                    <img src="" class="custom-carousel-image" alt="${cat.name}">
                </div>
                <div class="carousel-caption d-none d-md-block" style="background-color: #00000073">
                    <h5 style="color:#f3e9de">${cat.name}</h5>
                    <p style="color:#f3e9de">${truncateText(
											cat.description,
											200
										)}</p>
                </div>
            `

			carouselInner.appendChild(slide)
		})

		if (typeof bootstrap !== 'undefined') {
			new bootstrap.Carousel(document.getElementById('carouselExampleCaptions'))
		}
	} catch (error) {
		console.error('Ошибка загрузки данных карусели:', error)
		document.getElementById('carouselExampleCaptions').innerHTML = `
            <div class="alert alert-warning text-center">
                Ошибка загрузки данных карусели.
                <button class="btn btn-sm btn-primary" onclick="location.reload()">Попробовать снова</button>
            </div>
        `
	}
})

function truncateText(text, maxLength) {
	return text.length > maxLength
		? text.substring(0, maxLength - 3) + '...'
		: text
}
