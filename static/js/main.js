$(function () {
    lightbox.option({
        'resizeDuration': 200,
        'wrapAround': true
    });

    var hoverTimeout;
    $('.skay-cart').hover(
        function () {
            clearTimeout(hoverTimeout);
            $('.skay-cart_table').show();
        },
        function () {
            hoverTimeout = setTimeout(function () {
                $('.skay-cart_table').hide();
            }, 300);
        }
    )
});