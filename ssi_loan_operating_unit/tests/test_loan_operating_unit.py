# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestLoanOperatingUnit(YamlTransactionCase):
    def test_loan_operating_unit(self):
        self.run_yaml_scenario("test_data_loan_operating_unit.yaml")
