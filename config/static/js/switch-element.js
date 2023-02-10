function switch_element(client){
    var currentNode = document.querySelector('#flexable-div');

    // Logs the element and it's content into the console
    console.log(currentNode.outerHTML);

    if (client == 1){
    currentNode.outerHTML =
        '<div class="add2cart-buttons" id="flexable-div">' +
            '<button class="go2cart">Перейти в корзину</button>' +
            '<button onclick="switch_element(2);" class="minus">-</button>' +
            '<span class="count-of-product-in-cart">1</span>' +
            '<button class="plus">+</button>' +
        '</div>';
    }
    else{
        if (document.querySelector('.count-of-product-in-cart').innerHTML == 1){
            currentNode.outerHTML = 
            '<div class="add2cart-buttons" id="flexable-div">' +
                '<button onclick="switch_element(1)" class="add2cart-in-productcard">Добавить в корзину</button>' +
            '</div>';
        } 
    }
}