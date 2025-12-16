### Liskov Substitution Principle (LSP)
**Challenge:** Continuing from the refactored OrderProcessor class that adheres to the Open/Closed Principle. Now it is needed to ensure that any new payment gateway can seamlessly replace the existing ones without breaking the application.

a new CryptoPayment class is created to handle cryptocurrency payments.

**Problem**
```python
class CryptoPayment(PaymentStrategy):
    def process_payment(self, total, client_id):
        # ERROR: Crypto doesn't support client_id!
        raise Exception("Crypto payments require a wallet address, not a client ID!")
```

**Why is this a problem?**
The CryptoPayment class cannot be used interchangeably with other PaymentStrategy subclasses because it violates the expected behavior defined in the base class.

**The Solution (LSP Compliant):**
specific data should be handled within each subclass without breaking the contract established by the base class.

the `OrderProcessor` should not care how a payment is made (whether it needs a wallet, a card, or an API key). It only cares that the payment is made.

```python
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, total_amount):
        pass
class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
    def process_payment(self, total_amount):
        return f"Processing crypto payment of ${total_amount} to wallet {self.wallet_address}"

class StripePayment(PaymentStrategy):
    def __init__(self, client_id):
        self.client_id = client_id
    def process_payment(self, total_amount):
        return f"Processing stripe payment of ${total_amount} for client {self.client_id}"
```

**Don't create a child class that breaks the promise of the parent.**

*"Wherever the code expects a Parent (A), it must be able to accept the Child (B) without blowing up."*

**In the code:**

* **A (The Parent/Type): PaymentStrategy**
* **B (The Child/Subtype): CryptoPayment, StripePayment**
* **The code (the client): OrderProcessor**