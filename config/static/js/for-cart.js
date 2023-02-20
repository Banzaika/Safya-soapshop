function toggle(source){
    checkboxes = document.getElementsByName('boo');
    for(var i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = source.checked;
    }
    change_checkout_block();
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
    var count = document.getElementById('count-of-'+id);
    if (count.innerHTML > 1){
    count.innerHTML--;
    change2cart(id, csrftoken, 'decrease');
    }
    change_common_price();
}

function plus(id, csrftoken){
    var count = document.getElementById('count-of-'+id);
    count.innerHTML++;
    change2cart(id, csrftoken, 'increase'); 
    change_common_price();

}

function remove(id, csrftoken){
    var block = document.querySelector('#product-block-' + id);
    console.log(block);
    console.log(id);
    block.remove();
    var product_blocks = document.querySelectorAll('.product-block-in-cart');
    console.log(product_blocks);
    if (product_blocks.length == 0){
        console.log('hui');
        document.querySelector('.product-list-in-cart').innerHTML = '<div class="empty-cart-info">В вашей корзине ещё нет товаров</div>';
        document.querySelector('.checkout-block').remove();
        document.querySelector('.select2all').remove();
    }
    change2cart(id, csrftoken, 'clear');
}


function check(checkbox,id){
    // toggle all-box checkbox
    if (!checkbox.checked){
        document.querySelector('#all-box').checked = false;
    }
    change_checkout_block()
    change_common_price();
}

function change_common_price() {
    var checkedBoxes = document.querySelectorAll('input[name="boo"]:checked');
    // summing of common price
    var sum = 0;
    for (var i = 0; i < checkedBoxes.length; i++) {
        box_id = checkedBoxes[i].id
        var price = Number(document.querySelector(".price-value-" + box_id).innerHTML);
        var count = document.querySelector("#count-of-" + box_id).innerHTML;
        sum += price*count;
    }
    document.querySelector('.common-price').innerHTML = sum;
}

function change_checkout_block(){
        // change checkout block's view
        var checkedBoxes = document.querySelectorAll('input[name="boo"]:checked');
        var yourcart = document.querySelector('.your-cart');
        var common_price = document.querySelector('.common-price-block');
        var button = document.querySelector('.go2checkout');
        var inscription = document.querySelector('.need2select');
        var checkout_block = document.querySelector('.checkout-block');
        if (checkedBoxes.length == 0){
            yourcart.style.display = 'none';
            common_price.style.display = 'none';
            button.style.display = 'none';
            inscription.style.display = 'inline';
            checkout_block.style.height = '100px';
        }
        else {
            yourcart.style.display = 'inline';
            common_price.style.display = 'flex';
            button.style.display = 'block';
            inscription.style.display = 'none';
            checkout_block.style.height = '175px';
        }
}

function checkout(csrftoken){
    var checkedBoxes = document.querySelectorAll('input[name="boo"]:checked');
    var relation_ides = [];
    for (var i = 0; i < checkedBoxes.length; i++) {
        relation_ides.push(checkedBoxes[i].value);
    }
    console.log(relation_ides);
    fetch('http://127.0.0.1:8000/cart/checkout',{
          method: 'POST',
          redirect: 'follow',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          },
          body: relation_ides
        })
        .then((data) => {
          if(data.redirected){
            location.href = data.url;
          }
          });
        
}