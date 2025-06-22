$(document).ready(function() {

    $('#search').on('input', function() {
        var searchText = $(this).val().toLowerCase();
        $('.product').each(function() {
            var productName = $(this).data('name').toLowerCase();
            if (productName.includes(searchText)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    $('.add-to-cart').on('click', function() {
        alert('Товар додано до корзини!');
    });

    $('.product').hover(function() {
        $(this).css('transform', 'scale(1.1)');
    }, function() {
        $(this).css('transform', 'scale(1)');
    });
});