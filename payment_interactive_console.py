import requests
from hashlib import sha256

# Статус платежа после инициации - NEW
# Статус платежа после отмены - CANCELED
# Статус платежа после оплаты - CONFIRMED
# Статус оплаченного платежа после отмены - REFUNDED


class Payment:
    URL = "https://securepay.tinkoff.ru/v2/"
    TERMINAL_KEY = "TinkoffBankTest"

    def __init__(self, amount, order_id):
        self.payment_amount = amount
        self.order_id = order_id
        self.payment_id = ""

    @staticmethod
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

    def set_payment_id(self, payment_id):
        self.payment_id = payment_id

    def init_payment(self):
        init_json = {
            "TerminalKey": self.TERMINAL_KEY,
            "Amount": self.payment_amount,
            "OrderId": self.order_id,
            "Token": self.get_token(TerminalKey=self.TERMINAL_KEY, Amount=self.payment_amount, OrderId=self.order_id),
        }

        # Инициируем платеж
        initiate_payment = requests.post(f"{self.URL}Init", json=init_json)
        init_data = initiate_payment.json()

        # Проверка на ошибку запроса
        if not init_data['Success']:
            raise requests.exceptions.RequestException(
                f"Init Error Code {init_data['ErrorCode']}, details: {init_data['Details']}"
            )

        self.set_payment_id(init_data['PaymentId'])

        return init_data

    def cancel_payment(self):
        cancel_json = {
            "TerminalKey": self.TERMINAL_KEY,
            "PaymentId": self.payment_id,
            "Token": self.get_token(TerminalKey=self.TERMINAL_KEY, PaymentId=self.payment_id)
        }

        cancel_payment = requests.post(f"{self.URL}Cancel", json=cancel_json)
        cancel_data = cancel_payment.json()

        # Проверка на ошибку запроса
        if not cancel_data['Success']:
            raise requests.exceptions.RequestException(
                f"Cancel Error Code {cancel_data['ErrorCode']}, details: {cancel_data['Details']}"
            )

        return cancel_data

    def get_payment_status(self):
        payment_status_after_init = requests.post(
            f"{self.URL}GetState", json={
                "TerminalKey": self.TERMINAL_KEY,
                "PaymentId": self.payment_id,
                "Token": self.get_token(TerminalKey=self.TERMINAL_KEY, PaymentId=self.payment_id)
            }
        )

        print(f"Payment {self.payment_id} status: {payment_status_after_init.json()['Status']}")


while True:
    amount = input("To initiate payment enter amount: \n")
    order_id = input("To initiate payment enter order id: \n")
    new_payment = Payment(int(amount), order_id)
    data = new_payment.init_payment()
    new_payment.get_payment_status()
    print(f"Payment link: {data['PaymentURL']}")
    check_status = input("To check payment status enter 'status'\n")
    if check_status == "status":
        new_payment.get_payment_status()
        check_again = True
        while check_again:
            check = input("Check status again? Type 'yes' or 'no'\n")
            if check.lower() == 'no':
                check_again = False
            new_payment.get_payment_status()
        user_input = input("To cancel payment enter 'cancel'\nTo initiate new payment enter 'new'\n")
        if user_input.lower() == "cancel":
            new_payment.cancel_payment()
            new_payment.get_payment_status()
        if user_input.lower() == "new":
            continue
