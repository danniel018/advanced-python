"""
module to implement Liskov Substitution Principle (LSP) example
refactoring the Open/Closed Principle (OCP) example in the open_closed.md file.
"""

from abc import ABC
from abc import abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, total_amount: float):
        pass


class StripePayment(PaymentStrategy):
    def __init__(self, client_id: str):
        self.client_id = client_id

    def process_payment(self, total_amount: float):
        print("Connecting to Stripe...")
        print(f"Charging account {self.client_id} for ${total_amount}")


class PaypalPayment(PaymentStrategy):
    def __init__(self, client_id: str):
        self.client_id = client_id

    def process_payment(self, total_amount: float):
        print("Connecting to PayPal...")
        print(f"Charging account {self.client_id} for ${total_amount}")


class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def process_payment(self, total_amount: float):
        print("Connecting to Crypto Gateway...")
        print(f"Charging wallet {self.wallet_address} for ${total_amount}")


class OrderCalculator:
    def calculate_total(self, items):
        return sum(item["price"] * item["quantity"] for item in items)


class DatabaseOrderProcessor:
    def insert_order(self, order_id, total):
        print("Connecting to PostgreSQL...")
        print(f"INSERT INTO orders (id, total) VALUES ({order_id}, {total})")


class EmailProcessor:
    def send_confirmation(self, user_email):
        # In a real app, connection params might go in __init__
        print("Connecting to SMTP server...")
        print(f"Sending confirmation email to {user_email}")


class FileLogger:
    def log(self, message):
        with open("app.log", "a") as f:
            f.write(f"{message}\n")


# refactor orderProcessor to include paymentStrategy


class OrderProcessor:
    def __init__(
        self,
        calculator: OrderCalculator,
        database: DatabaseOrderProcessor,
        email: EmailProcessor,
        logger: FileLogger,
        payment_gateway: PaymentStrategy,
    ):
        self.order_calculator = calculator
        self.database_order_processor = database
        self.email_processor = email
        self.logger = logger
        self.payment_gateway = payment_gateway

    def process_order(self, order_id, items, user_email):
        total = self.order_calculator.calculate_total(items)
        self.payment_gateway.process_payment(total)
        self.database_order_processor.insert_order(order_id, total)
        self.email_processor.send_confirmation(user_email)
        self.logger.log(f"Order {order_id} processed with total ${total}")


# Example usage:if __name__ == "__main__":
items = [{"price": 10.0, "quantity": 2}, {"price": 5.0, "quantity": 1}]
calculator = OrderCalculator()
database = DatabaseOrderProcessor()
email = EmailProcessor()
logger = FileLogger()
payment_gateway = StripePayment(client_id="client_123")

order_processor = OrderProcessor(
    calculator,
    database,
    email,
    logger,
    payment_gateway,
)
order_processor.process_order(
    order_id=1, items=items, user_email="john.doe@example.com"
)
