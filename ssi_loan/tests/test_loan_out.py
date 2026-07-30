# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestLoanOut(YamlTransactionCase):
    """Cover the ``loan.out`` lifecycle end-to-end via YAML scenario."""

    def test_loan_out(self):
        """Run the ``test_data_loan_out.yaml`` scenario."""
        self.run_yaml_scenario("test_data_loan_out.yaml")
