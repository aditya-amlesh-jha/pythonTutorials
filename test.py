from flask import Flask, render_template, request

app = Flask(__name__)

class BankAccount:
    def __init__(self,name,balance):
        self.name = name
        self.transactions = []
        self.balance = balance
    
    def deposit(self,amount):
        self.balance += amount
        self.transactions.append({"deposit":amount})
        return self.balance
    
    def withdraw(self,amount):
        if amount > self.balance:
            return "Insufficient funds"
        self.balance -= amount
        self.transactions.append({"withdraw":amount})
        return self.balance

    def return_balance(self):
      return f"Balance is :: {self.balance}"

    def get_transactions(self):
        return self.transactions
    
    def __str__(self):
      return f"Account Name: {self.name}\nAccount Balance: {self.balance}\n"
     

class Bank:
    def __init__(self):
        self.accounts = {}
        self.key = 0
    
    def add_account(self,account):
        self.accounts[self.key] = account
        self.key += 1
    
    def get_account(self,account_number):
        if account_number not in self.accounts:
            return "No account by that number"
        return self.accounts[account_number]
    
    def remove_account(self,account_number):
        if account_number not in self.accounts:
            return "No account by that number"
        del self.accounts[account_number]
        return "Account removed"

    def withdraw(self,account_number,amount):
        if account_number not in self.accounts:
            return "No account by that number"
        return self.accounts[account_number].withdraw(amount)
    
    def deposit(self,account_number,amount):
        if account_number not in self.accounts:
            return "No account by that number"
        return self.accounts[account_number].deposit(amount)

    def check_balance(self,account_number):
        if account_number not in self.accounts:
            return "No account by that number"
        return self.accounts[account_number].return_balance()

    def get_transaction_history(self,account_number):
      account = bank.get_account(account_number)
      res = ""
      if account:
          transactions = account.get_transactions()
          print("Transaction History for Account 1:")
          for transaction in transactions:
              for key, value in transaction.items():
                  res+=f"{key.capitalize()}: {value}\n"
      else:
          res+="Account does not exist"
      return res
    
    def __str__(self):
        res = ""
        for i in self.accounts:
            res += f"Account Number {i}\n"+(self.accounts[i]).__str__()+"\n"
        return res

# Create bank object
bank = Bank()

# Sample data for accounts
bank.add_account(BankAccount("John", 1000))
bank.add_account(BankAccount("Alice", 2000))
bank.add_account(BankAccount("Bob", 500))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/accounts')
def view_accounts():
    return render_template('accounts.html', accounts=bank.accounts)

@app.route('/account/<int:account_number>', methods=['GET', 'POST'])
def account_details(account_number):
    account = bank.get_account(account_number)
    if account is None:
        return "Account not found"
    
    if request.method == 'POST':
        amount = int(request.form['amount'])
        action = request.form['action']
        
        if action == 'deposit':
            account.deposit(amount)
        elif action == 'withdraw':
            account.withdraw(amount)
    
    return render_template('account_details.html', account=account)

if __name__ == '__main__':
    app.run()