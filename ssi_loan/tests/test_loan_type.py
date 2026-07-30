# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestLoanType(YamlTransactionCase):
    """Cover ``loan.type`` master data CRUD via YAML scenario."""

    def test_loan_type(self):
        """Run the ``test_data_loan_type.yaml`` scenario."""
        self.run_yaml_scenario("test_data_loan_type.yaml")
