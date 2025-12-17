### Dependency Inversion Principle (DIP)
**Challenge:** Continuing from the refactored NotificationProcessor class that adheres to the Interface Segregation Principle. Now it is needed to ensure that high-level modules do not depend on low-level modules but rather on abstractions.

**the DIP states:**
* *High-level modules should not depend on low-level modules. Both should depend on abstractions (interfaces).*
* *Abstractions should not depend on details; details should depend on abstractions.*

```python
# current state

class OrderProcessor:
    def __init__(
        self,
        calculator: OrderCalculator, #Concrete class
        database: DatabaseOrderProcessor, #Concrete class
        notification_processor: NotificationProcessor, #Concrete class
        logger: FileLogger, #Concrete class
        payment_gateway: PaymentStrategy, #Abstraction
        client_id: str = "client_123",
    ):
```
**OrderProcessor** (a high-level module) depends directly on several low-level modules (concrete classes like `DatabaseOrderProcessor`, `FileLogger`, etc.). This creates tight coupling and makes the system less flexible.

state 1 is respected in payment_gateway since it depends on the abstraction PaymentStrategy.

**The problem:**

if FileLogger was needed to be replaced with a different logging mechanism, the OrderProcessor class would need to be modified, violating the Open/Closed Principle.

**The Solution (DIP Compliant):**
```python
# Abstractions for low-level modules
class Logger(ABC):
    @abstractmethod
    def log(self, message):
        pass

class CloudLogger(Logger):
    def log(self, message):
        #implementation for cloud logging
        pass

class DatabaseProcessor(ABC):
    @abstractmethod
    def insert_order(self, order_id, total):
        pass
class CloudDatabaseProcessor(DatabaseProcessor):
    def insert_order(self, order_id, total):
        #implementation for cloud database
        pass
class OrderProcessor:
    def __init__(
        self,
        calculator: OrderCalculator, #Concrete class
        database: DatabaseProcessor, #Abstraction
        notification_processor: NotificationProcessor, #Concrete class
        logger: Logger, #Abstraction
        payment_gateway: PaymentStrategy, #Abstraction
        client_id: str = "client_123",
    ):
        