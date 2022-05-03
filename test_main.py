from main import Account, Atm
from unittest import TestCase
from unittest.mock import patch



class TestAccount(TestCase):
    def test_authorize(self):
        account1 = Account(1434597300, 1234, 100)
        self.assertEqual(account1.authorize(1234), True)

    def test_authorize_for_wrong_pin(self):
        account1 = Account(1434597300, 1234, 100)
        self.assertEqual(account1.authorize(4321), False)

    def test_get_balance(self):
        self.assertEqual(Account(1434597300, 1234, 100).getBalance(), 100)

    def test_withdraw(self):
        account1 = Account(1434597300, 1234, 100)
        account1.withdraw(100)
        self.assertEqual(account1.getBalance(), 0)

    @patch('builtins.print')
    def test_withdraw_for_overdraft(self, mock_print):
        account1 = Account(1434597300, 1234, 100)
        account1.withdraw(106)
        output_list = ["Amount dispensed: $106", "You have been charged an overdraft fee of $5. Current balance: -11"]
        output_index = 0
        # self.assertEqual(account1.getBalance(), 0)

        for call in mock_print.call_args_list:
            args, kwargs = call
            self.assertEqual(output_list[output_index], args[0])
            output_index += 1

    def test_deposit(self):
        account1 = Account(1434597300, 1234, 100)
        account1.deposit(20)
        self.assertEqual(account1.getBalance(), 120)

    @patch('builtins.print')
    def test_print_history_for_no_history(self, mock_print):
        account1 = Account(1434597300, 1234, 100)
        account1.printHistory()
        mock_print.assert_called_with('No history found')

    @patch('builtins.print')
    def test_print_history(self, mock_print):
        account1 = Account(1434597300, 1234, 100)
        account1.deposit(20)
        account1.withdraw(100)
        account1.printHistory()
        output_list = ["Current balance: 120", "Amount dispensed: $100", "Current balance: 20", " -100 20", " 20 120"]
        output_index = 0

        for call in mock_print.call_args_list:
            args, kwargs = call
            self.assertTrue(output_list[output_index] in args[0])
            output_index += 1

    @patch('builtins.print')
    def test_logout(self, mock_print):
        account1 = Account(1434597300, 1234, 100)
        account1.logout()
        mock_print.assert_called_with('Account 1434597300 logged out.')

    @patch('builtins.print')
    def test_atm_authorize_for_no_account(self, mock_print):
        atm = Atm()
        atm.loadAccountData('account_details.csv')
        atm.authorize("authorize 6434597300 4557".split())

        output_list = ["Authorization failed."]
        output_index = 0

        for call in mock_print.call_args_list:
            args, kwargs = call
            self.assertEqual(output_list[output_index], args[0])
            output_index += 1

    @patch('builtins.print')
    def test_atm_authorize(self, mock_print):
        atm = Atm()
        atm.loadAccountData('account_details.csv')
        atm.authorize("authorize 1434597300 4557".split())

        output_list = ["1434597300 successfully authorized."]
        output_index = 0

        for call in mock_print.call_args_list:
            args, kwargs = call
            self.assertEqual(output_list[output_index], args[0])
            output_index += 1

    def test_isAuthorize(self):
        atm = Atm()
        atm.loadAccountData('account_details.csv')
        self.assertFalse(atm.isAuthorized())

        atm.authorize("authorize 1434597300 4557".split())
        self.assertTrue(atm.isAuthorized())

        atm.logout()
        self.assertFalse(atm.isAuthorized())

    @patch('builtins.print')
    def test_atm_logout_no_loggedin_acc_user(self, mock_print):
        atm = Atm()
        atm.loadAccountData('account_details.csv')
        atm.logout()

        output_list = ["No account is currently authorized."]
        output_index = 0

        for call in mock_print.call_args_list:
            args, kwargs = call
            self.assertEqual(output_list[output_index], args[0])
            output_index += 1

    def test_atm_logout_loggedin_acc_user(self):
        atm = Atm()
        atm.loadAccountData('account_details.csv')
        atm.authorize("authorize 1434597300 4557".split())
        atm.logout()
        self.assertEqual(None,  atm._Atm__current_user)

    @patch('builtins.print')
    def test_atm_withdraw(self, mock_print):
        atm = Atm()
        atm.loadAccountData('account_details.csv')
        atm.authorize("authorize 1983738828 7676".split())
        atm.withdraw("withdraw 100".split())

        output_list = ["1983738828 successfully authorized.", "Your account is overdrawn! You may not make withdrawals at this time."]
        output_index = 0

        for call in mock_print.call_args_list:
            args, kwargs = call
            self.assertEqual(output_list[output_index], args[0])
            output_index += 1

    @patch('builtins.print')
    def test_atm_withdraw_multiple(self,mock_print):
        atm = Atm()
        atm.loadAccountData('account_details.csv')
        atm.authorize("authorize 1434597300 4557".split())
        atm.withdraw("withdraw 11".split())

        output_list = ["1434597300 successfully authorized.",
                       "Withdrawal amount must be a multiple of 20."]
        output_index = 0

        for call in mock_print.call_args_list:
            args, kwargs = call
            self.assertEqual(output_list[output_index], args[0])
            output_index += 1

    @patch('builtins.print')
    def test_atm_withdraw_unable_to_process(self, mock_print):
        atm = Atm()
        atm.loadAccountData('account_details.csv')
        atm.authorize("authorize 1873628978 3398".split())
        atm.withdraw("withdraw 10020.00".split())
        atm.withdraw("withdraw 20.00".split())

        output_list = ["1873628978 successfully authorized.", "Unable to dispense full amount requested at this time.", "Amount dispensed: $10000.0", "Current balance: 99999990000.0"]
        output_index = 0

        for call in mock_print.call_args_list:
            args, kwargs = call
            if output_index >= len(output_list):
                pass
            else:
                self.assertEqual(output_list[output_index], args[0])
            output_index += 1

    @patch('builtins.print')
    def test_atm_withdraw_(self, mock_print):
        atm = Atm()
        atm.loadAccountData('account_details.csv')
        atm.authorize("authorize 1434597300 4557".split())
        atm.withdraw("withdraw 20.00".split())

        output_list = ["1434597300 successfully authorized.","Amount dispensed: $20.0", "Current balance: 89980.55"]
        output_index = 0

        for call in mock_print.call_args_list:
            args, kwargs = call
            if output_index >= len(output_list):
                pass
            else:
                self.assertEqual(output_list[output_index], args[0])
            output_index += 1

    @patch('builtins.print')
    def test_atm_balance(self, mock_print):
        atm = Atm()
        atm.loadAccountData('account_details.csv')
        atm.authorize("authorize 1434597300 4557".split())
        atm.balance()

        output_list = ["1434597300 successfully authorized.", "Current balance: 90000.55"]
        output_index = 0

        for call in mock_print.call_args_list:
            args, kwargs = call
            self.assertEqual(output_list[output_index], args[0])
            output_index += 1