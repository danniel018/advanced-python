"""Factory pattern to create concrete payment strategy objects for
`OrderProcessor` without coupling it to specific payment providers."""

from strategies import PaymentStrategyV3


# Factory
class PaymentFactory:
    def __init__(self):
        self.__strategies = {}

    def set_strategies(self, strategies: dict):
        self.__strategies = strategies

    def register_strategy(self, name: str, strategy: PaymentStrategyV3):
        self.__strategies[name] = strategy

    def create_payment(self, payment: str, **kwargs) -> PaymentStrategyV3:
        strategy_class = self.__strategies.get(payment)
        if not strategy_class:
            raise ValueError(f"Payment method '{payment}' is not supported.")
        return strategy_class(**kwargs)


class OrderProcessorV5:
    def __init__(
        self,
        payment: PaymentStrategyV3,
    ):
        self.payment = payment

    def process_order(self):
        # Simulate order total calculation
        print("[V5] Processing order ")


def main():
    client_id = "client_123"

    payment = PaymentFactory.create_payment("stripe", client_id=client_id)

    orderProcessor = OrderProcessorV5(
        payment=payment,
    )
    orderProcessor.process_order()
