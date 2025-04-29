ymaps.ready(init);

function init(){
    let map = new ymaps.Map('map',{
        center: [59.929370148727195,30.34904127923608],
        zoom: 17,
    });

    let placemark = new ymaps.Placemark([59.92923931204485,30.348037602667628], {},);

    map.geoObjects.add(placemark);
}