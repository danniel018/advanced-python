"""
module to implement dependency inversion principle (DIP) example
refactoring the Interface Segregation Principle (ISP) example in the
interface_segregation.md file.
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


class EmailSender(ABC):
    @abstractmethod
    def send_email(self, message):
        pass

class SMSSender(ABC):
    @abstractmethod
    def send_sms(self, message):
        pass

class SlackSender(ABC):
    @abstractmethod
    def send_slack_message(self, message):
        pass

class NotificationProcessor(EmailSender, SMSSender):
    def send_email(self, message):
        #implementation
        print("Connecting to SMTP server...")
        print(f"Sending email: {message}")
    def send_sms(self, message):
        #implementation
        print("Connecting to SMS gateway...")
        print(f"Sending SMS: {message}")

class Logger(ABC):
    @abstractmethod
    def log(self, message):
        pass

class CloudLogger(Logger):

    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def log(self, message):
        print("Connecting to Cloud Logging Service...")
        print(f"Logging message: {message}")

class FileLogger(Logger):
    def log(self, message):
        with open("app.log", "a") as f:
            f.write(f"{message}\n")

class OrderRepository(ABC):
    @abstractmethod
    def insert_order(self, order_id, total):
        pass

class PostgreSQLOrderRepository(OrderRepository):
    def insert_order(self, order_id, total):
        print("Connecting to PostgreSQL...")
        print(f"INSERT INTO orders (id, total) VALUES ({order_id}, {total})")

class OrderProcessor:
    def __init__(
        self,
        calculator: OrderCalculator,
        database: OrderRepository,
        notification_processor: NotificationProcessor,
        logger: Logger,
        payment_gateway: PaymentStrategy,
    ):
        self.order_calculator = calculator
        self.database_order_processor = database
        self.notification_processor = notification_processor
        self.logger = logger
        self.payment_gateway = payment_gateway

    def process_order(self, order_id, items, user_email):
        total = self.order_calculator.calculate_total(items)
        self.payment_gateway.process_payment(total)
        self.database_order_processor.insert_order(order_id, total)
        self.notification_processor.send_email(f"Order {order_id} confirmed.")
        self.logger.log(f"Order {order_id} processed with total ${total}")

# Example usage:
if __name__ == "__main__":
    items = [{"price": 10.0, "quantity": 2}, {"price": 5.0, "quantity": 1}]
    calculator = OrderCalculator()
    database = PostgreSQLOrderRepository()
    notification_processor = NotificationProcessor()
    logger = FileLogger()
    payment_gateway = StripePayment(client_id="client_123")

    order_processor = OrderProcessor(
        calculator,
        database,
        notification_processor,
        logger,
        payment_gateway,
    )

    order_processor.process_order(
        order_id="order_456",
        items=items,
        user_email="user@example.com",
    )
