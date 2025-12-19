"""
module for the implementation of different payment strategies
using the Strategy Pattern.
This pattern complements the Factory Pattern in pattern.py
"""

from abc import ABC, abstractmethod


class PaymentStrategyV3(ABC):
    @abstractmethod
    def process_payment(self, total: float):
        pass


class StripePaymentV3(PaymentStrategyV3):
    def __init__(self, client_id: str):
        self.client_id = client_id

    def process_payment(self, total: float):
        print(f"[V3] Stripe: Charging {self.client_id} for ${total}")


class CryptoPaymentV3(PaymentStrategyV3):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def process_payment(self, total: float):
        print(f"[V3] Crypto: Charging {self.wallet_address} for ${total}")


STRATEGIES = {
    "stripe": StripePaymentV3,
    "crypto": CryptoPaymentV3,
}
