import time
import requests
from hashlib import sha256

# Статус платежа после инициации - NEW
# Статус платежа после отмены - CANCELED
# Статус платежа после оплаты - CONFIRMED
# Статус оплаченного платежа после отмены - REFUNDED


# Функция для создания токена
def get_token(**kwargs):
    kwargs["Password"] = "TinkoffBankTest"
    sorted_parameters = sorted(kwargs.items())
    string_for_hash = ""
    for item in sorted_parameters:
        value = item[1]
        if type(item[1]) != str:
            value = str(item[1])
        string_for_hash += value
    return sha256(string_for_hash.encode('utf-8')).hexdigest()


URL = "https://securepay.tinkoff.ru/v2/"
TERMINAL_KEY = "TinkoffBankTest"
ORDER_ID = "1000980001008"


def init_payment(amount):
    """Инициация платежа"""
    init_json = {
        "TerminalKey": TERMINAL_KEY,
        "Amount": amount,
        "OrderId": ORDER_ID,
        "Token": get_token(TerminalKey=TERMINAL_KEY, Amount=amount, OrderId=ORDER_ID),
    }

    # Инициируем платеж
    initiate_payment = requests.post(f"{URL}Init", json=init_json)
    init_data = initiate_payment.json()

    # Проверка на ошибку запроса
    if not init_data['Success']:
        raise requests.exceptions.RequestException(
            f"Init Error Code {init_data['ErrorCode']}, details: {init_data['Details']}"
        )
    return init_data


def cancel_payment(payment_id):
    """Отмена платежа"""
    cancel_json = {
        "TerminalKey": TERMINAL_KEY,
        "PaymentId": payment_id,
        "Token": get_token(TerminalKey=TERMINAL_KEY, PaymentId=payment_id)
    }

    cancel_payment = requests.post(f"{URL}Cancel", json=cancel_json)
    cancel_data = cancel_payment.json()

    # Проверка на ошибку запроса
    if not cancel_data['Success']:
        raise requests.exceptions.RequestException(
            f"Cancel Error Code {cancel_data['ErrorCode']}, details: {cancel_data['Details']}"
        )

    return cancel_data


def get_payment_status(payment_id):
    """Получение статуса платежа"""
    payment_status_after_init = requests.post(
        f"{URL}GetState", json={
            "TerminalKey": TERMINAL_KEY,
            "PaymentId": payment_id,
            "Token": get_token(TerminalKey=TERMINAL_KEY, PaymentId=payment_id)
        }
    )

    print(f"Payment status: {payment_status_after_init.json()['Status']}")


# # Инициация платежа
init_data = init_payment(100000)
payment_id = init_data["PaymentId"]

# Статус платежа после инициации
get_payment_status(payment_id)

# Ссылка на проведение платежа
payment_url = init_data['PaymentURL']
print(payment_url)

# Время на оплату
time.sleep(240)
# Статус платежа после оплаты
get_payment_status(payment_id)

# Отмена платежа
cancel_payment(payment_id)
