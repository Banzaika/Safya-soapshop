function confirm2order(button, id, csrftoken) {
    if (confirm('Вы действительно хотите подтвердить получение?')) {
        button.innerHTML = 'Подтверждено';
        fetch('http://127.0.0.1:8000/delivery_confirmation', {
            method: 'POST',
            redirect: 'follow',
            headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            },
            body: id
        })

        .then((data) => {
            if(data.success){
            location.reload();
            }
            }
        );

    }
}
