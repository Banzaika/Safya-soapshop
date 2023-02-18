function switch_element(client){
    var big_button = document.querySelector('.add2cart-in-productcard');

    var go2cart = document.querySelector('.go2cart');
    var plus = document.querySelector('.plus');
    var minus = document.querySelector('.minus');
    var count = document.querySelector('.count-of-product-in-cart');
    if (client == 1){
        big_button.style.display = 'none';
        go2cart.style.display = 'block';
        plus.style.display = 'block';
        minus.style.display = 'block';
        count.style.display = 'inline';

    }
    else{
        if (document.querySelector('.count-of-product-in-cart').innerHTML < "1"){
            big_button.style.display = 'block';
            go2cart.style.display = 'none';
            plus.style.display = 'none';
            minus.style.display = 'none';
            count.style.display = 'none';
        } 
    }
}

function change2cart(id, csrftoken, path){
    fetch('http://127.0.0.1:8000/cart/' + path, {
          method: 'POST',
          redirect: 'follow',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          },
          body: id
        })
        .then((data) => {
          if(data.redirected){
            location.href = data.url;
          }
          });
    
}

function minus(id, csrftoken){
    change2cart(id, csrftoken, 'decrease');
    var count = document.querySelector('.count-of-product-in-cart');
    count.innerHTML--;
    switch_element(2);
}


function plus(id, csrftoken){
    var count = document.querySelector('.count-of-product-in-cart');
    count.innerHTML++;
    change2cart(id, csrftoken, 'increase'); 
}

function add2cart(id, csrftoken){
    change2cart(id, csrftoken, 'increase');
    switch_element(1);
    var count = document.querySelector('.count-of-product-in-cart');
    count.innerHTML = 1
}