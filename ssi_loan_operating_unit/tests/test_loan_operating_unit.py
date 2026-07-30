# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestLoanOperatingUnit(YamlTransactionCase):
    """Cover operating unit propagation on ``loan.out``/``loan.in``."""

    def test_loan_operating_unit(self):
        """Run the ``test_data_loan_operating_unit.yaml`` scenario."""
        self.run_yaml_scenario("test_data_loan_operating_unit.yaml")
