import uuid, json
from yookassa import Configuration, Payment

Configuration.account_id = '987633'
Configuration.secret_key = 'test_psc57gtbiDrzAf_qc1hT_2hjF8KiTfIIEB3WgW00qQw'

def create_payment(value, description):
    payment = Payment.create({
        "amount": {
            "value": str(value) + '.00',
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://f18b-31-130-148-166.eu.ngrok.io/orders"
        },
        "capture": True,
        "description": description,
        "test": True
    }, uuid.uuid4())

    payment_id = payment.id
    confirmation_url = payment.confirmation.confirmation_url
    return payment_id, confirmation_url