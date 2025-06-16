$(document).ready(function () {

    $('#right').click(function(){
        const left = document.querySelector(".container-cards");
        left.scrollBy(500, 0, { behavior: 'smooth'});
    });

    $('#left').click(function(){
        const right = document.querySelector(".container-cards");
        right.scrollBy(-500, 0, { behavior: 'smooth'});
    });

});