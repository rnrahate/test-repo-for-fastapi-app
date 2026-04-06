from app.calculations import add, BankAccount
import pytest

@pytest.fixture
def zero_bank_account():
    print("\nCreating a zero balance bank account for testing...")
    return BankAccount()

@pytest.fixture
def bank_account():
    print("\nCreating a bank account with a initial balance of 50 for testing...")
    return BankAccount(50)

@pytest.mark.parametrize("num1,num2,expected", [
    (5, 3, 8),
    (0, 0, 0),
    (-1, 1, 0)
])
def test_addition(num1, num2, expected):
    print("Testing addition function...")

    assert add(num1, num2) == expected
    print("Addition test passed!")

# testing bank account with zero balance
def test_bank_account(zero_bank_account):
    print("Testing BankAccount class...")

    account = zero_bank_account
    assert account.balance == 0
    print("Initial balance test passed!")

    account.deposit(100)
    assert account.balance == 100
    print("Deposit test passed!")
    
    account.withdraw(30)
    assert account.balance == 70
    print("Withdrawal test passed!")

    with pytest.raises(ValueError):
        account.withdraw(100)
    print("Overdraft test passed!")

    account.collect_interest()
    assert round(account.balance, 2) == 73.5
    print("Interest collection test passed!")

    print("BankAccount tests passed!")

# testing bank account with 50 balance
def test_bank_account_with_balance(bank_account):

    print("Testing BankAccount class with initial balance...")

    print("Testing deposit functionality...")
    account = bank_account
    print("Initial balance:", account.balance)

    account.deposit(50)
    assert account.balance == 100
    print("Deposit test passed!")
    print("Testing withdrawal functionality...")

    account.withdraw(20)
    assert account.balance == 80
    print("Withdrawal test passed!")

    print("Testing interest collection functionality...")
    account.collect_interest()
    assert round(account.balance, 2) == 84.0
    print("Interest collection test passed!")

    print("BankAccount tests with initial balance passed!")

@pytest.mark.parametrize("deposit,withdraw,expected", [
    (500, 300, 200),
    (120, 20, 100),
    (100, 1, 99)
])
def test_bank_transactions(zero_bank_account, deposit, withdraw, expected):
    print("Testing multiple transactions on BankAccount...")

    account = zero_bank_account
    print("Initial balance:", account.balance)

    account.deposit(deposit)
    print("Balance after deposit of {}:".format(deposit), account.balance)

    account.withdraw(withdraw)
    print("Balance after withdrawal of {}:".format(withdraw), account.balance)

    with pytest.raises(ValueError):
        account.withdraw(account.balance + 1)  # Attempt to withdraw more than the current balance
    print("Overdraft test passed!, Insufficient amount")

    account.collect_interest()
    amount = expected * 1.05
    assert round(account.balance, 2) == amount
    print("Interest collection test passed!")

    print("Multiple transactions test passed!")

def test_insufficient_funds(bank_account):
    account = bank_account
    with pytest.raises(ValueError):
        account.withdraw(100)
    print("Insufficient funds!",f"\nTotal balance: {account.balance} \nWithdraw amount: 100")

