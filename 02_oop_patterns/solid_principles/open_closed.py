"""
module to implement Open/Closed Principle (OCP) example
adding stripe processor support to OrderProcessor 
through paymentStrategy and concrete implementations
"""
from abc import ABC

class PaymentStrategy(ABC):

    def process_payment(self):
        pass


class StripePayment(PaymentStrategy):

    def process_payment(self):
        return "processing with stripe"
    

class PaypalPayment(PaymentStrategy):

    def process_payment(self):
        return "processing with paypal"
    

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
        client_id: str = "client_123",
    ):
        self.order_calculator = calculator
        self.database_order_processor = database
        self.email_processor = email
        self.logger = logger
        self.payment_gateway = payment_gateway
        self.client_id = client_id

    def process_order(self, order_id, items, user_email):
        total = self.order_calculator.calculate_total(items)

        self.payment_gateway.process_payment(
            self.payment_gateway, total, self.client_id
        )

        self.database_order_processor.insert_order(order_id,total)

        self.email_processor.send_confirmation(user_email)

        self.logger.log("Order processed")
