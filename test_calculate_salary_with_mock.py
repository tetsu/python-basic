import unittest
from unittest.mock import MagicMock
from unittest import mock

import calculate_salary


class TestSalary(unittest.TestCase):

    def test_calculate_salary(self):
        s = calculate_salary.Salary(year=2017)
        s.bonus_api.bonus_price = MagicMock(return_value=1)
        self.assertEqual(s.calculate_salary(), 101)
        s.bonus_api.bonus_price.assert_called()
        s.bonus_api.bonus_price.assert_called_once()
        s.bonus_api.bonus_price.assert_called_with(year=2017)
        s.bonus_api.bonus_price.assert_called_once_with(year=2017)
        self.assertEqual(s.bonus_api.bonus_price.call_count, 1)

    def test_calculate_salary_no_salary(self):
        s = calculate_salary.Salary(year=2050)
        s.bonus_api.bonus_price = MagicMock(return_value=0)
        self.assertEqual(s.calculate_salary(), 100)
        s.bonus_api.bonus_price.assert_not_called()

    @mock.patch('calculate_salary.ThirdPartyBonusRestApi.bonus_price', return_value=1)
    def test_calculate_salary_patch(self, mock_bonus):
        s = calculate_salary.Salary(year=2017)
        self.assertEqual(s.calculate_salary(), 101)
        mock_bonus.assert_called()

    def test_calculate_salary_patch_with(self):
        with mock.patch('calculate_salary.ThirdPartyBonusRestApi.bonus_price') as mock_bonus:
            mock_bonus.return_value = 1
            s = calculate_salary.Salary(year=2017)
            salary_price = s.calculate_salary()
            self.assertEqual(salary_price, 101)
            mock_bonus.assert_called()

    # def test_calculate_salary_patch_patcher(self):
    #     patcher = mock.patch('calculate_salary.ThirdPartyBonusRestApi.bonus_price')
    #     mock_bonus = patcher.start()
    #     mock_bonus.return_value = 1
    #     s = calculate_salary.Salary(year=2017)
    #     salary_price = s.calculate_salary()
    #     self.assertEqual(salary_price, 101)
    #     mock_bonus.assert_called()
    #     patcher.stop()

    def setUp(self):
        self.patcher = mock.patch('calculate_salary.ThirdPartyBonusRestApi.bonus_price')
        self.mock_bonus = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_calculate_salary_patch_patcher(self):
        self.mock_bonus.return_value = 1
        s = calculate_salary.Salary(year=2017)
        salary_price = s.calculate_salary()
        self.assertEqual(salary_price, 101)
        self.mock_bonus.assert_called()

    def test_calculate_salary_patch_side_effect(self):
        # def f(year):
        #     return 1
        self.mock_bonus.side_effect = lambda year: 1
        s = calculate_salary.Salary(year=2017)
        salary_price = s.calculate_salary()
        self.assertEqual(salary_price, 101)
        self.mock_bonus.assert_called()

    def test_calculate_salary_patch_side_effect_refused(self):
        # def f(year):
        #     return 1
        self.mock_bonus.side_effect = ConnectionRefusedError
        s = calculate_salary.Salary(year=2017)
        salary_price = s.calculate_salary()
        self.assertEqual(salary_price, 100)
        self.mock_bonus.assert_called()

    def test_calculate_salary_patch_side_effect_list(self):
        self.mock_bonus.side_effect = [
            1,
            2,
            3,
            ValueError('Bankrupt!!!')
        ]
        s = calculate_salary.Salary(year=2017)
        salary_price = s.calculate_salary()
        self.assertEqual(salary_price, 101)

        s = calculate_salary.Salary(year=2018)
        salary_price = s.calculate_salary()
        self.assertEqual(salary_price, 102)

        s = calculate_salary.Salary(year=2019)
        salary_price = s.calculate_salary()
        self.assertEqual(salary_price, 103)

        s = calculate_salary.Salary(year=200)
        with self.assertRaises(ValueError):
            s.calculate_salary()

        self.mock_bonus.assert_called()


if __name__ == "__main__":
    unittest.main()