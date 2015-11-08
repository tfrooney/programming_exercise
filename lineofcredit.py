"""
Create an implementation of the following:

A line of credit product.  This is like a credit card except theres no card.
It should work like this:

  - Have a built in APR and credit limit
  - Be able to draw ( take out money ) and make payments.
  - Keep track of principal balance and interest on the line of credit
  - APR Calculation based on the outstanding principal balance over real number of days.
  - Interest is not compounded, so it is only charged on outstanding principal.
  - Keep track of transactions such as payments and draws on the line and when
    they occured.
  - 30 day payment periods.  Basically what this means is that interest will not be
    charged until the closing of a 30 day payment period.  However, when it is charged,
    it should still be based on the principal balance over actual number of days outstanding
    during the period, not just ending principal balance.

Couple of Scenarios how it would play out:

Scenario 1:

Someone creates a line of credit for 1000$ and 35% APR.

He draws 500$ on day one so his remaining credit limit is 500$ and his balance is 500$.
He keeps the money drawn for 30 days.  He should owe 500$ * 0.35 / 365 * 30 = 14.38$ worth
of interest on day 30.  Total payoff amount would be 514.38$

Scenario 2:

Someone creates a line of credit for 1000$ and 35% APR.

He draws 500$ on day one so his remaining credit limit is 500$ and his balance is 500$.
He pays back 200$ on day 15 and then draws another 100$ on day 25.  His total owed interest on
day 30 should be 500 * 0.35 / 365 * 15 + 300 * 0.35 / 365 * 10 + 400 * 0.35 / 365 * 5  which is
11.99.  Total payment should be 411.99.
    """


class CreditAccount(object):
    """
    Account tracking line of credit

    Attributes
        credit_limit
        interest_rate
        balance
        transactions

    """

    def __init__(self, txn_svc, acct_id, rate, limit):
        self.txn_svc = txn_svc
        self.account_id = acct_id
        self.interest_rate = rate
        self.credit_limit = limit
        self.balance = 0
        self.finance_charges = 0.0

    def close_30day_period(self):
        self.balance = self.balance * self.interest_rate

    def show_balance(self):
        print 'balance:' + '${0:.2f}'.format(self.balance) + ' acct:' + str(self.account_id)

    def show_finance_charges(self):
        print 'finance charges:' + '${0:.2f}'.format(self.finance_charges) + ' acct:' + str(self.account_id)

    def show_total_payment(self):
        print 'Account:' + str(self.account_id) + ' Total Payment:' + '${0:.2f}'.format(self.balance + self.finance_charges)


class Transaction(object):
    """
    Track activity on an account

    Attributes
        account_id
        day
        amount
    """

    def __init__(self, acct_id, day, amount):
        self.account_id = acct_id
        self.day = day
        self.amount = amount

    def get_acct(self):
        return self.account_id

    def get_day(self):
        return self.day

    def get_amount(self):
        return self.amount


class TransactionService(object):

    def __init__(self, period):
        self.period = period
        self.transactions = []

    def withdraw(self, acct, day, amount):
        print 'Account:' + str(acct.account_id) + ' Withdraw:' + '${0:.2f}'.format(amount)
        if acct.credit_limit >= (acct.balance + acct.finance_charges + amount):
            acct.balance = acct.balance + amount
            t = Transaction(acct.account_id, day, amount)
            self.insert_transaction(t)
        else:
            print 'ERROR: Exceeded Credit Limit'

    def payment(self, acct, day, amount):
        print 'Account:' + str(acct.account_id) + ' Payment:' + '${0:.2f}'.format(amount)
        if 0 <= (acct.balance + acct.finance_charges) - amount:
            acct.balance = acct.balance - amount
            t = Transaction(acct.account_id, day, 0 - amount)
            self.insert_transaction(t)
        else:
            print 'ERROR: Exceeded Balance Owed'

    def insert_transaction(self, txn):
        self.transactions.append(txn)

    def show_transactions(self, acct_id):
        print 'transactions: ' + ' acct:' + str(acct_id) + ' '
        for txn in self.transactions:
            if txn.get_acct() == acct_id:
                print ' day:' + str(txn.get_day()) + ' amt:' + str(txn.get_amount())

    def charge_interest(self, acct):
        """
        run at the end of the payment period
        balance * rate / days in year * days for each balance level
        """
        print 'Charge Interest'
        interest = 0
        start_day_of_balance = 0
        balance = 0
        for txn in self.transactions:
            if txn.get_acct() == acct.account_id:
                days = txn.get_day() - start_day_of_balance
                interest = balance * acct.interest_rate / 365 * days
                start_day_of_balance = txn.get_day()
                balance += txn.get_amount()
                acct.finance_charges += interest
                #print 'txn:' + str(txn.get_day()) + ' days:' + str(days) + ' int:' + str(interest) + ' fin:' + str(acct.finance_charges) + ' firstday:' + str(start_day_of_balance) + ' bal:' + str(balance) + ' amt:' + str(txn.get_amount())

        days = self.period - start_day_of_balance
        acct.finance_charges += balance * acct.interest_rate / 365 * days
        #print 'acct:' + str(acct.account_id) + ' days:' + str(days) + ' int:' + str(interest) + ' fin:' + str(acct.finance_charges) + ' firstday:' + str(start_day_of_balance) + ' bal:' + str(balance) + ' amt:' + str(txn.get_amount())

    def reset_period(self):
        # preceding period transactions could be archived
        self.transactions = []


def test_harness():
    ts = TransactionService(30)
    acct1 = CreditAccount(ts, 1, 0.30, 1000)
    ts.withdraw(acct1, 1, 300)
    ts.withdraw(acct1, 5, 300)
    ts.withdraw(acct1, 5, 1300)
    ts.payment(acct1, 10, 600)
    ts.payment(acct1, 10, 600)
    acct1.show_balance()
    acct2 = CreditAccount(ts, 2, 0.30, 2000)
    ts.withdraw(acct2, 10, 300)
    acct2.show_balance()
    ts.show_transactions(1)
    ts.show_transactions(2)
    ts.charge_interest(acct1)
    acct1.show_balance()
    acct1.show_finance_charges()
    ts.charge_interest(acct2)
    acct2.show_balance()
    acct2.show_finance_charges()
    acct2.show_total_payment()

    ex1 = CreditAccount(ts, 3, 0.35, 1000)
    ts.withdraw(ex1, 0, 500)
    ts.charge_interest(ex1)
    ex1.show_total_payment()

    ex2 = CreditAccount(ts, 4, 0.35, 1000)
    ts.withdraw(ex2, 0, 500)
    ts.payment(ex2, 15, 200)
    ts.withdraw(ex2, 25, 100)
    ts.charge_interest(ex2)
    ex2.show_total_payment()


if __name__ == "__main__":
    test_harness()


















