### Single Responsibility Principle:
**Problem:**

Here is an OrderProcessor class. It works, but it's a nightmare to maintain.
This is a class that knows too much and does too much.

If the marketing team decides to change the email subject line, we have to open this file. If the DevOps team changes the database password, we have to open the same file.

```python
class OrderProcessor:
    def process_order(self, order_id, items, user_email):
        # 1. Calculate logic
        total = 0
        for item in items:
            total += item['price'] * item['quantity']
        
        # 2. Payment logic
        print(f"Connecting to Stripe...")
        print(f"Charging credit card for ${total}")
        
        # 3. Database logic
        print(f"Connecting to PostgreSQL...")
        print(f"INSERT INTO orders (id, total) VALUES ({order_id}, {total})")
        
        # 4. Notification logic
        print(f"Connecting to SMTP server...")
        print(f"Sending confirmation email to {user_email}")
        
        # 5. Logging logic
        with open('app.log', 'a') as f:
            f.write(f"Order {order_id} processed successfully.\n")
```
**Distinct Responsibilities:**
1. Calculating order totals
2. Processing payments
3. Interacting with the database
4. Sending notifications
5. Logging events