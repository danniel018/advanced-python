### Interface Segregation Principle (ISP)
**Challenge:** Continuing from the refactored PaymentStrategy interface that adheres to the Liskov Substitution Principle. Now it is needed to ensure that clients are not forced to depend on methods they do not use.

Currently, there is a general notification interface. depending on the notification type, some clients would need to implement methods they don't use (e.g., SMS notifications for email-only clients).

support for SMS, email, and Slack notifications must be added.

**Why is this important?**

IPS promotes decoupling and flexibility by ensuring that clients only depend on the methods they actually use. This leads to cleaner, more maintainable code.

ISP avoids "fat" interfaces that force clients to implement unnecessary methods and creates unintended coupling.


```python
#specific interfaces for each notification type
from abc import ABC, abstractmethod
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

class FullNotificationProcessor(EmailSender, SMSSender, SlackSender):
    def send_email(self, message):
        #implementation
    def send_sms(self, message):
        #implementation
    def send_slack_message(self, message):
        #implementation
class EmailOnlyNotificationProcessor(EmailSender):
    def send_email(self, message):
        #implementation
```