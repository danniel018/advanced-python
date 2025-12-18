# SOLID Principles - Order Processing System

This module demonstrates SOLID principles through incremental refactoring of an `OrderProcessor` class. Each principle builds on the previous one, transforming a monolithic design into clean, maintainable architecture.

---

## 📁 Folder Structure

```
solid_principles/

├── order_processor_evolution.py         # 🔄 V0→V5 evolution in one file
│
├── single_responsibility.py/.md         # S - Split responsibilities
├── open_closed.py/.md                   # O - Strategy pattern
├── liskov_substitution.py/.md           # L - Unified signatures
├── interface_segregation.py/.md         # I - Focused interfaces
└── dependency_inversion.py/.md          # D - Abstract dependencies
```

---

## 🔄 Evolution Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        OrderProcessor Evolution                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  V0: MONOLITH                                                               │
│  ┌─────────────────────────────────────────┐                                │
│  │ OrderProcessor                          │                                │
│  │  - calculate total                      │  ← All 5 responsibilities      │
│  │  - process payment (Stripe hardcoded)   │    in ONE class                │
│  │  - save to database (PostgreSQL)        │                                │
│  │  - send email                           │                                │
│  │  - log events                           │                                │
│  └─────────────────────────────────────────┘                                │
│                          │                                                  │
│                          ▼ SRP                                              │
│  V1: SPLIT RESPONSIBILITIES                                                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                         │
│  │ Calculator   │ │ Payment      │ │ Database     │                         │
│  └──────────────┘ └──────────────┘ └──────────────┘                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                         │
│  │ Email        │ │ Logger       │ │ Orchestrator │                         │
│  └──────────────┘ └──────────────┘ └──────────────┘                         │
│                          │                                                  │
│                          ▼ OCP                                              │
│  V2: STRATEGY PATTERN                                                       │
│           ┌──────────────────────┐                                          │
│           │ «ABC» PaymentStrategy│                                          │
│           └──────────┬───────────┘                                          │
│          ┌───────────┼───────────┐                                          │
│          ▼           ▼           ▼                                          │
│  ┌─────────────┐ ┌─────────┐ ┌─────────┐                                    │
│  │ Stripe      │ │ PayPal  │ │ + New   │  ← Add without modifying           │
│  └─────────────┘ └─────────┘ └─────────┘                                    │
│                          │                                                  │
│                          ▼ LSP                                              │
│  V3: UNIFIED SIGNATURES                                                     │
│  ┌─────────────────────────────────────────────────────────┐                │
│  │ process_payment(total)  ← Same signature for ALL        │                │
│  │                                                         │                │
│  │ Credentials (client_id, wallet_address) in __init__     │                │
│  └─────────────────────────────────────────────────────────┘                │
│                          │                                                  │
│                          ▼ ISP                                              │
│  V4: FOCUSED INTERFACES                                                     │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐                               │
│  │ EmailSender│ │ SMSSender  │ │ SlackSender│  ← Pick what you need         │
│  └────────────┘ └────────────┘ └────────────┘                               │
│                          │                                                  │
│                          ▼ DIP                                              │
│  V5: ALL ABSTRACTIONS (FINAL)                                               │
│  ┌─────────────────────────────────────────────────────────┐                │
│  │ OrderProcessor depends on:                              │                │
│  │   • PaymentStrategy (ABC)                               │                │
│  │   • OrderRepository (ABC)  ← Not PostgreSQL             │                │
│  │   • Logger (ABC)           ← Not FileLogger             │                │
│  │   • EmailSender (ABC)      ← Not SMTPEmailer            │                │
│  └─────────────────────────────────────────────────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Principles Summary

### **S - Single Responsibility Principle (SRP)**
> A class should have only one reason to change.

**File:** `single_responsibility.py`

Split the monolithic `OrderProcessor` into:
- `OrderCalculator` - calculates totals
- `PaymentProcessor` - handles payments
- `DatabaseOrderProcessor` - persistence
- `EmailProcessor` - notifications
- `FileLogger` - logging

---

### **O - Open/Closed Principle (OCP)**
> Open for extension, closed for modification.

**File:** `open_closed.py`

Replace `if/elif` payment logic with `PaymentStrategy` ABC:
- Add new payment methods by creating new classes
- No modification to existing code

---

### **L - Liskov Substitution Principle (LSP)**
> Subtypes must be substitutable for their base types.

**File:** `liskov_substitution.py`

Fix: Move payment-specific data (client_id, wallet_address) to `__init__`:
- All strategies have identical `process_payment(total)` signature
- `CryptoPayment` works just like `StripePayment`

---

### **I - Interface Segregation Principle (ISP)**
> Clients should not depend on interfaces they don't use.

**File:** `interface_segregation.py`

Split fat `NotificationService` into focused interfaces:
- `EmailSender` - only email
- `SMSSender` - only SMS
- `SlackSender` - only Slack
- Classes implement only what they need

---

### **D - Dependency Inversion Principle (DIP)**
> Depend on abstractions, not concretions.

**File:** `dependency_inversion.py`

`OrderProcessor` now depends on:
- `OrderRepository` (ABC) instead of `PostgreSQLDatabase`
- `Logger` (ABC) instead of `FileLogger`
- Swap implementations without changing `OrderProcessor`

---

## 🚀 Quick Start

```python
# Run the complete evolution demo
python order_processor_evolution.py

# Or import specific versions
from solid_principles import OrderProcessorV5, StripePaymentV3

processor = OrderProcessorV5(
    calculator=OrderCalculatorV5(),
    repository=PostgreSQLRepositoryV5(),
    notifier=EmailNotifierV4(),
    logger=CloudLoggerV5(),
    payment=StripePaymentV3(client_id="stripe_123"),
)
processor.process_order("order_001", items, "user@example.com")
```

---
