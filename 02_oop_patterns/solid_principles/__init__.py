"""
SOLID Principles - OrderProcessor Evolution

This package demonstrates the incremental application of SOLID principles
to refactor a monolithic OrderProcessor into a clean, maintainable design.

Quick Start:
    from solid_principles import OrderProcessorV5, StripePaymentV3, ...

    processor = OrderProcessorV5(
        calculator=OrderCalculatorV5(),
        repository=PostgreSQLRepositoryV5(),
        notifier=EmailNotifierV4(),
        logger=FileLoggerV5(),
        payment=StripePaymentV3(client_id="..."),
    )

Versions:
    V0: Monolith (violates all principles)
    V1: After SRP - Split responsibilities
    V2: After OCP - Strategy pattern for payments
    V3: After LSP - Unified method signatures
    V4: After ISP - Focused notification interfaces
    V5: After DIP - All dependencies are abstractions (FINAL)

Structure:
    solid_principles/
    ├── before/                         # "Bad" examples showing violations
    │   ├── order_processor_monolith.py
    │   ├── payment_processor_ocp_violation.py
    │   ├── payment_strategy_lsp_violation.py
    │   ├── notification_isp_violation.py
    │   └── order_processor_dip_violation.py
    ├── after/                          # Clean implementations
    │   ├── abstractions.py             # All ABC interfaces
    │   ├── implementations.py          # Concrete classes
    │   └── order_processor_final.py    # Complete working example
    ├── order_processor_evolution.py    # V0→V5 in one file
    ├── single_responsibility.py        # SRP principle
    ├── open_closed.py                  # OCP principle
    ├── liskov_substitution.py          # LSP principle
    ├── interface_segregation.py        # ISP principle
    └── dependency_inversion.py         # DIP principle
"""

# Export evolution versions for easy comparison
from .order_processor_evolution import (
    # V0: Monolith
    OrderProcessorV0,
    # V1: After SRP
    OrderProcessorV1,
    OrderCalculatorV1,
    PaymentProcessorV1,
    DatabaseV1,
    EmailProcessorV1,
    FileLoggerV1,
    # V2: After OCP
    OrderProcessorV2,
    PaymentStrategyV2,
    StripePaymentV2,
    PaypalPaymentV2,
    # V3: After LSP
    OrderProcessorV3,
    PaymentStrategyV3,
    StripePaymentV3,
    CryptoPaymentV3,
    # V4: After ISP
    OrderProcessorV4,
    EmailSenderV4,
    SMSSenderV4,
    EmailNotifierV4,
    MultiNotifierV4,
    # V5: After DIP (Final)
    OrderProcessorV5,
    OrderRepositoryV5,
    LoggerV5,
    PostgreSQLRepositoryV5,
    MongoDBRepositoryV5,
    FileLoggerV5,
    CloudLoggerV5,
    OrderCalculatorV5,
)

__all__ = [
    # Version 0
    "OrderProcessorV0",
    # Version 1 - SRP
    "OrderProcessorV1",
    "OrderCalculatorV1",
    "PaymentProcessorV1",
    "DatabaseV1",
    "EmailProcessorV1",
    "FileLoggerV1",
    # Version 2 - OCP
    "OrderProcessorV2",
    "PaymentStrategyV2",
    "StripePaymentV2",
    "PaypalPaymentV2",
    # Version 3 - LSP
    "OrderProcessorV3",
    "PaymentStrategyV3",
    "StripePaymentV3",
    "CryptoPaymentV3",
    # Version 4 - ISP
    "OrderProcessorV4",
    "EmailSenderV4",
    "SMSSenderV4",
    "EmailNotifierV4",
    "MultiNotifierV4",
    # Version 5 - DIP (Final)
    "OrderProcessorV5",
    "OrderRepositoryV5",
    "LoggerV5",
    "PostgreSQLRepositoryV5",
    "MongoDBRepositoryV5",
    "FileLoggerV5",
    "CloudLoggerV5",
    "OrderCalculatorV5",
]
