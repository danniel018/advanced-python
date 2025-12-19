# Factory Pattern

The factory pattern centralizes object creation so the caller only asks for a product by name and receives a fully configured instance. This keeps construction logic in one place and keeps the rest of the code unaware of concrete classes.

## How it is implemented here

- `PaymentFactory` holds a registry mapping a payment method name to a concrete `PaymentStrategyV3` class (see `strategies.py`).
- New strategies are registered via `set_strategies()` for a whole mapping or `register_strategy()` for one-off additions.
- `create_payment()` validates the requested method and instantiates the strategy with any keyword arguments.
- `OrderProcessorV5` depends on the abstract `PaymentStrategyV3`, so swapping payment providers does not require changing the processor.

## Usage

```python
from factory.pattern import PaymentFactory
from factory.strategies import STRATEGIES

factory = PaymentFactory()
factory.set_strategies(STRATEGIES)

payment = factory.create_payment("stripe", client_id="client_123")
payment.process_payment(total=49.99)
```

## Adding a new payment method

1. Implement a new class that inherits from `PaymentStrategyV3` and implements `process_payment`.
2. Register it: `factory.register_strategy("paypal", PaypalPaymentV3)`.
3. Call `factory.create_payment("paypal", **kwargs)` where needed.

## When to reach for a factory

- You have multiple concrete implementations that share an interface and you want a single entry point to obtain them.
- Object construction needs extra setup and you want to avoid sprinkling that logic across the codebase.
- You expect to add or swap implementations over time without touching call sites.
