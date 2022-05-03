

import csv
import time
import datetime


class Account:

    def __init__(self, account_id, pin, balance=0):
        self.__account_id = account_id
        self.__pin = pin
        self.__balance = balance
        self.__transactions = []
        self.__last_transaction_time = None

    def authorize(self, pin):
        if pin == self.__pin:
            self.updateActivity()
            print('{0} successfully authorized.'.format(self.__account_id))
            return True
        print('Authorization failed.')
        return False

    def updateActivity(self):
        self.__last_transaction_time = time.time()

    def isTimeOut(self):
        time_diff = int(time.time() - self.__last_transaction_time)
        return time_diff > 120

    def logout(self):
        self.__last_transaction_time = None
        print('Account {0} logged out.'.format(self.__account_id))

    def isOverDrawn(self):
        return self.__balance < 0

    def getBalance(self):
        return self.__balance

    def withdraw(self, amount):
        print('Amount dispensed: ${0}'.format(amount))
        if amount > self.getBalance():
            amount = amount + 5
            self.__balance = self.__balance - amount
            print('You have been charged an overdraft fee of $5. Current balance: {0}'.format(self.getBalance()))
        else:
            self.__balance = self.__balance - amount
            print('Current balance: {0}'.format(self.getBalance()))
        self.addTransaction(-1 * amount)

    def deposit(self, amount):
        self.__balance = self.__balance + amount
        print('Current balance: {0}'.format(self.getBalance()))
        self.addTransaction(amount)

    def addTransaction(self, amount):
        str_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__transactions.insert(0, '{0} {1} {2}'.format(str_time, amount, self.getBalance()))
        self.updateActivity()

    def printHistory(self):
        self.updateActivity()
        if len(self.__transactions) == 0:
            print('No history found')
            return

        for trans in self.__transactions:
            print(trans)


class Atm:

    def __init__(self):
        self.__amount = float('10000')
        self.__accounts_map = {}
        self.__current_user = None

    def loadAccountData(self, account_details_path):
        with open(account_details_path, 'r') as account_file:
            account_csv = csv.reader(account_file)
            header = next(account_csv)
            for row in account_csv:
                account_id = row[0]
                account_pin = row[1]
                account_balance = float(row[2])
                new_account = Account(account_id, account_pin, account_balance)
                self.__accounts_map[account_id] = new_account

    def run(self):

        while True:
            command = str(input()).split()

            if command[0] == 'authorize':
                self.authorize(command)
            elif command[0] == 'logout':
                pass
            elif command[0] == 'end':
                break
            elif command[0] in ['withdraw', 'deposit', 'balance', 'history']:
                if not self.isAuthorized():
                    print('Authorization required.')
                    continue

                if command[0] == 'withdraw':
                    self.withdraw(command)
                elif command[0] == 'deposit':
                    self.deposit(command)
                elif command[0] == 'balance':
                    self.balance()
                elif command[0] == 'history':
                    self.history()

    def authorize(self, command):
        account_id = str(command[1])
        pin = str(command[2])

        if account_id not in self.__accounts_map:
            print('Authorization failed.')
            return

        if self.__accounts_map[account_id].authorize(pin):
            self.__current_user = self.__accounts_map[account_id]

    def isAuthorized(self):
        if self.__current_user is None:
            return False
        if self.__current_user.isTimeOut():
            self.logout()
            return False
        return True

    def logout(self):
        if self.__current_user is None:
            print('No account is currently authorized.')
            return
        self.__current_user.logout()
        self.__current_user = None

    def withdraw(self, command):
        amount = float(command[1])
        if self.__current_user.isOverDrawn():
            print('Your account is overdrawn! You may not make withdrawals at this time.')
            return

        if float(str(amount)) % float('20') != 0:
            print('Withdrawal amount must be a multiple of 20.')
            return

        if self.__amount <= 0:
            print('Unable to process your withdrawal at this time.')
            return

        if self.__amount < amount:
            amount = self.__amount
            print('Unable to dispense full amount requested at this time.')
        self.__current_user.withdraw(amount)

    def deposit(self, command):
        amount = float(command[1])
        self.__current_user.deposit(amount)
        self.__amount = self.__amount + amount

    def balance(self):
        amount = self.__current_user.getBalance()
        self.__current_user.updateActivity()
        print('Current balance: {0}'.format(amount))

    def history(self):
        self.__current_user.printHistory()


if __name__ == '__main__':
    atm = Atm()
    atm.loadAccountData('account_details.csv')
    atm.run()
