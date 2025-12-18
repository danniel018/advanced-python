"""
OrderProcessor Evolution: From Monolith to SOLID

This file shows the complete journey of refactoring an OrderProcessor
through all five SOLID principles. Each version builds on the previous.

V0: Monolith (violates all principles)
V1: After SRP - Split into single-responsibility classes
V2: After OCP - PaymentStrategy pattern for extensibility
V3: After LSP - Unified method signatures for substitutability
V4: After ISP - Focused notification interfaces
V5: After DIP - All dependencies are abstractions

Run this file to see each version in action:
    python order_processor_evolution.py
"""
from abc import ABC, abstractmethod


# ============================================================================
# V0: THE MONOLITH (Before any SOLID principles)
# ============================================================================

class OrderProcessorV0:
    """
    The original monolithic class that violates ALL SOLID principles.

    Problems:
    - SRP ❌ Has 5 responsibilities: calculation, payment, db, email, logging
    - OCP ❌ Adding payment gateways requires modifying this class
    - LSP ❌ N/A (no inheritance yet)
    - ISP ❌ N/A (no interfaces yet)
    - DIP ❌ Hardcoded dependencies (Stripe, PostgreSQL, etc.)
    """

    def process_order(self, order_id, items, user_email):
        # 1. Calculate total
        total = sum(item["price"] * item["quantity"] for item in items)

        # 2. Process payment (hardcoded Stripe)
        print(f"[V0] Connecting to Stripe... Charging ${total}")

        # 3. Save to database (hardcoded PostgreSQL)
        print(f"[V0] INSERT INTO orders VALUES ({order_id}, {total})")

        # 4. Send email
        print(f"[V0] Sending email to {user_email}")

        # 5. Log
        print(f"[V0] Logged: Order {order_id} processed")

        return total


# ============================================================================
# V1: AFTER SRP (Single Responsibility Principle)
# ============================================================================

class OrderCalculatorV1:
    """SRP: Only calculates totals."""
    def calculate_total(self, items):
        return sum(item["price"] * item["quantity"] for item in items)


class PaymentProcessorV1:
    """SRP: Only handles payments."""
    def process_payment(self, gateway, total, client_id):
        print(f"[V1] {gateway}: Charging {client_id} for ${total}")


class DatabaseV1:
    """SRP: Only handles persistence."""
    def insert_order(self, order_id, total):
        print(f"[V1] INSERT INTO orders VALUES ({order_id}, {total})")


class EmailProcessorV1:
    """SRP: Only sends emails."""
    def send_confirmation(self, user_email):
        print(f"[V1] Sending confirmation to {user_email}")


class FileLoggerV1:
    """SRP: Only handles logging."""
    def log(self, message):
        print(f"[V1] LOG: {message}")


class OrderProcessorV1:
    """
    SRP ✅ Orchestrates workflow, delegates to specialized classes.

    Still violates:
    - OCP ❌ PaymentProcessorV1 uses if/elif for gateways
    - DIP ❌ Depends on concrete classes
    """

    def __init__(self):
        self.calculator = OrderCalculatorV1()
        self.payment = PaymentProcessorV1()
        self.database = DatabaseV1()
        self.email = EmailProcessorV1()
        self.logger = FileLoggerV1()

    def process_order(self, order_id, items, user_email):
        total = self.calculator.calculate_total(items)
        self.payment.process_payment("Stripe", total, "client_123")
        self.database.insert_order(order_id, total)
        self.email.send_confirmation(user_email)
        self.logger.log(f"Order {order_id} processed")
        return total


# ============================================================================
# V2: AFTER OCP (Open/Closed Principle)
# ============================================================================

class PaymentStrategyV2(ABC):
    """OCP: Abstract base for payment strategies."""
    @abstractmethod
    def process_payment(self, total: float, client_id: str):
        pass


class StripePaymentV2(PaymentStrategyV2):
    """OCP: New payment method without modifying existing code."""
    def process_payment(self, total: float, client_id: str):
        print(f"[V2] Stripe: Charging {client_id} for ${total}")


class PaypalPaymentV2(PaymentStrategyV2):
    """OCP: Another payment method - no modification needed."""
    def process_payment(self, total: float, client_id: str):
        print(f"[V2] PayPal: Charging {client_id} for ${total}")


class OrderProcessorV2:
    """
    SRP ✅ Single responsibility
    OCP ✅ Extensible via PaymentStrategy

    Still violates:
    - LSP ❌ client_id in method breaks CryptoPayment
    - DIP ❌ Still uses concrete classes for db, email, logger
    """

    def __init__(self, payment: PaymentStrategyV2):
        self.calculator = OrderCalculatorV1()
        self.payment = payment
        self.database = DatabaseV1()
        self.email = EmailProcessorV1()
        self.logger = FileLoggerV1()
        self.client_id = "client_123"

    def process_order(self, order_id, items, user_email):
        total = self.calculator.calculate_total(items)
        self.payment.process_payment(total, self.client_id)
        self.database.insert_order(order_id, total)
        self.email.send_confirmation(user_email)
        self.logger.log(f"Order {order_id} processed")
        return total


# ============================================================================
# V3: AFTER LSP (Liskov Substitution Principle)
# ============================================================================

class PaymentStrategyV3(ABC):
    """LSP: Unified signature - credentials in __init__, not process_payment."""
    @abstractmethod
    def process_payment(self, total: float):
        pass


class StripePaymentV3(PaymentStrategyV3):
    def __init__(self, client_id: str):
        self.client_id = client_id

    def process_payment(self, total: float):
        print(f"[V3] Stripe: Charging {self.client_id} for ${total}")


class CryptoPaymentV3(PaymentStrategyV3):
    """LSP ✅ Same signature as other strategies - wallet in __init__."""
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def process_payment(self, total: float):
        print(f"[V3] Crypto: Charging {self.wallet_address} for ${total}")


class OrderProcessorV3:
    """
    SRP ✅ Single responsibility
    OCP ✅ Extensible via PaymentStrategy
    LSP ✅ All PaymentStrategy implementations are substitutable

    Still violates:
    - ISP ❌ EmailProcessor might need to implement unused methods
    - DIP ❌ Still depends on concrete classes
    """

    def __init__(self, payment: PaymentStrategyV3):
        self.calculator = OrderCalculatorV1()
        self.payment = payment
        self.database = DatabaseV1()
        self.email = EmailProcessorV1()
        self.logger = FileLoggerV1()

    def process_order(self, order_id, items, user_email):
        total = self.calculator.calculate_total(items)
        self.payment.process_payment(total)
        self.database.insert_order(order_id, total)
        self.email.send_confirmation(user_email)
        self.logger.log(f"Order {order_id} processed")
        return total


# ============================================================================
# V4: AFTER ISP (Interface Segregation Principle)
# ============================================================================

class EmailSenderV4(ABC):
    """ISP: Focused interface for email only."""
    @abstractmethod
    def send_email(self, message: str):
        pass


class SMSSenderV4(ABC):
    """ISP: Focused interface for SMS only."""
    @abstractmethod
    def send_sms(self, message: str):
        pass


class EmailNotifierV4(EmailSenderV4):
    """ISP ✅ Implements only what it needs."""
    def send_email(self, message: str):
        print(f"[V4] Email: {message}")


class MultiNotifierV4(EmailSenderV4, SMSSenderV4):
    """ISP ✅ Implements multiple interfaces by choice, not force."""
    def send_email(self, message: str):
        print(f"[V4] Email: {message}")

    def send_sms(self, message: str):
        print(f"[V4] SMS: {message}")


class OrderProcessorV4:
    """
    SRP ✅ Single responsibility
    OCP ✅ Extensible via PaymentStrategy
    LSP ✅ All strategies are substitutable
    ISP ✅ Focused notification interfaces

    Still violates:
    - DIP ❌ Still depends on concrete OrderCalculator, Database, Logger
    """

    def __init__(self, payment: PaymentStrategyV3, notifier: EmailSenderV4):
        self.calculator = OrderCalculatorV1()  # Concrete!
        self.payment = payment
        self.database = DatabaseV1()  # Concrete!
        self.notifier = notifier
        self.logger = FileLoggerV1()  # Concrete!

    def process_order(self, order_id, items, user_email):
        total = self.calculator.calculate_total(items)
        self.payment.process_payment(total)
        self.database.insert_order(order_id, total)
        self.notifier.send_email(f"Order {order_id} confirmed!")
        self.logger.log(f"Order {order_id} processed")
        return total


# ============================================================================
# V5: AFTER DIP (Dependency Inversion Principle) - FINAL VERSION
# ============================================================================

class OrderRepositoryV5(ABC):
    """DIP: Abstraction for persistence."""
    @abstractmethod
    def insert_order(self, order_id: str, total: float):
        pass


class LoggerV5(ABC):
    """DIP: Abstraction for logging."""
    @abstractmethod
    def log(self, message: str):
        pass


class PostgreSQLRepositoryV5(OrderRepositoryV5):
    def insert_order(self, order_id: str, total: float):
        print(f"[V5] PostgreSQL: INSERT ({order_id}, {total})")


class MongoDBRepositoryV5(OrderRepositoryV5):
    def insert_order(self, order_id: str, total: float):
        print(f"[V5] MongoDB: insertOne({order_id}, {total})")


class FileLoggerV5(LoggerV5):
    def log(self, message: str):
        print(f"[V5] FileLog: {message}")


class CloudLoggerV5(LoggerV5):
    def log(self, message: str):
        print(f"[V5] CloudLog: {message}")


class OrderCalculatorV5:
    """Calculator - kept concrete as it has no external dependencies."""
    def calculate_total(self, items):
        return sum(item["price"] * item["quantity"] for item in items)


class OrderProcessorV5:
    """
    FINAL VERSION - All SOLID principles applied!

    SRP ✅ Single responsibility - orchestrates workflow
    OCP ✅ Extensible via PaymentStrategy - add new payments freely
    LSP ✅ All strategies are substitutable - same interface
    ISP ✅ Focused interfaces - clients implement only what they need
    DIP ✅ Depends on abstractions - swap any implementation
    """

    def __init__(
        self,
        calculator: OrderCalculatorV5,
        repository: OrderRepositoryV5,
        notifier: EmailSenderV4,
        logger: LoggerV5,
        payment: PaymentStrategyV3,
    ):
        self.calculator = calculator
        self.repository = repository
        self.notifier = notifier
        self.logger = logger
        self.payment = payment

    def process_order(self, order_id: str, items: list, user_email: str) -> float:
        total = self.calculator.calculate_total(items)
        self.payment.process_payment(total)
        self.repository.insert_order(order_id, total)
        self.notifier.send_email(f"Order {order_id} confirmed for {user_email}!")
        self.logger.log(f"Order {order_id} processed: ${total}")
        return total


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demo():
    """Run all versions to see the evolution."""
    items = [{"price": 10.0, "quantity": 2}, {"price": 5.0, "quantity": 1}]

    print("=" * 70)
    print("V0: MONOLITH (Before SOLID)")
    print("=" * 70)
    v0 = OrderProcessorV0()
    v0.process_order("001", items, "user@example.com")

    print("\n" + "=" * 70)
    print("V1: After SRP (Split responsibilities)")
    print("=" * 70)
    v1 = OrderProcessorV1()
    v1.process_order("001", items, "user@example.com")

    print("\n" + "=" * 70)
    print("V2: After OCP (PaymentStrategy pattern)")
    print("=" * 70)
    v2 = OrderProcessorV2(payment=StripePaymentV2())
    v2.process_order("001", items, "user@example.com")

    print("\n" + "=" * 70)
    print("V3: After LSP (Unified signatures - CryptoPayment works!)")
    print("=" * 70)
    v3 = OrderProcessorV3(payment=CryptoPaymentV3(wallet_address="0xABC123"))
    v3.process_order("001", items, "user@example.com")

    print("\n" + "=" * 70)
    print("V4: After ISP (Focused notification interfaces)")
    print("=" * 70)
    v4 = OrderProcessorV4(
        payment=StripePaymentV3(client_id="stripe_123"),
        notifier=MultiNotifierV4()
    )
    v4.process_order("001", items, "user@example.com")

    print("\n" + "=" * 70)
    print("V5: After DIP (All abstractions - FINAL)")
    print("=" * 70)
    v5 = OrderProcessorV5(
        calculator=OrderCalculatorV5(),
        repository=MongoDBRepositoryV5(),
        notifier=EmailNotifierV4(),
        logger=CloudLoggerV5(),
        payment=CryptoPaymentV3(wallet_address="0xDEF456"),
    )
    v5.process_order("001", items, "user@example.com")

    print("\n" + "=" * 70)
    print("EVOLUTION SUMMARY")
    print("=" * 70)
    print("""
    V0 → V1: Split monolith into 5 single-purpose classes (SRP)
    V1 → V2: Replace if/elif with Strategy pattern (OCP)
    V2 → V3: Move credentials to __init__ for uniform signatures (LSP)
    V3 → V4: Split fat interface into EmailSender + SMSSender (ISP)
    V4 → V5: Abstract remaining concrete dependencies (DIP)
    """)


if __name__ == "__main__":
    demo()
