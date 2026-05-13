class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal failed: Insufficient balance.")
        else:
            self.balance -= amount
            print(f"Withdrawal successful. New balance: ${self.balance}")


class SavingsAccount(BankAccount):
    def __init__(self, balance):
        super().__init__(balance)
        self.withdraw_limit = 100  # withdrawal limit for savings account

    # Overriding the parent withdraw method
    def withdraw(self, amount):
        if amount > self.withdraw_limit:
            print(f"Withdrawal failed: Maximum withdrawal limit is ${self.withdraw_limit}.")
        else:
            super().withdraw(amount)


# Example usage
account = SavingsAccount(500)

account.withdraw(80)    # allowed
account.withdraw(150)   # exceeds limit
account.withdraw(50)    # allowed
