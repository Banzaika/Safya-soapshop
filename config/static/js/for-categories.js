function switch_element(client, id) {
    var svg_img1 = document.querySelector('#add2cart1-' + id);
    var svg_img2 = document.querySelector('#add2cart2-' + id);

    if (client == 1){
        svg_img1.style.display = 'none';
        svg_img2.style.display = 'block';
    }
    else {
        svg_img1.style.display = 'block';
        svg_img2.style.display = 'none';
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

function switch_add(client, id, csrftoken){
    change2cart(id, csrftoken,  'increase');
    switch_element(client, id);
}

function switch_clear(client, id, csrftoken){
  change2cart(id, csrftoken, 'clear');
  switch_element(client, id);
}


function switch_remove(client, id, csrftoken){
  change2cart(id, csrftoken, 'decrease');
  switch_element(client, id);
}
