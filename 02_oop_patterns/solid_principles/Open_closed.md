### Open/Closed Principle (OCP)
**Challenge:** conitinuing from the refactored OrderProcessor class that adheres to the Single Responsibility Principle. Now it is needed to add support for a new payment gateway, such as PayPal and keep stripe as an option.

**bad approach:**
```python
class PaymentProcessor:
    def process_payment(self, gateway, total, client_id):
        if gateway == "Stripe":
            # Stripe logic
            pass
        elif gateway == "PayPal":
            # New PayPal logic
            pass
```

**why is this bad?**
1. a class that is already working is being modified (risk of breaking existing functionality)
2. if another payment gateway is added in the future, if/elif statements will keep growing, making the code harder to read and maintain.

**The Solution (OCP Compliant):**

Instead of one concrete class doing everything, a common Contract (Interface) is defined and separated classes for each payment method.

An abstract base class called PaymentBase (or PaymentStrategy) forces any subclass to have a process_payment method

**Why is this "Open/Closed"?**

Open for Extension: If we want to add CryptoPayment, we just create a new class class CryptoPayment(PaymentStrategy).

Closed for Modification: We do not touch OrderProcessor. It just works.