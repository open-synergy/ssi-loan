# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestLoanSecurity(YamlTransactionCase):
    """Cover ``loan.in``/``loan.out`` ACL and record rule scoping.

    Regression coverage for the ``model_id`` mix-up between
    ``access_loan_in_all`` / ``loan_in_self_rule`` and ``loan.out``
    (open-synergy/ssi-loan#89).
    """

    def test_loan_security(self):
        """Run the ``test_data_loan_security.yaml`` scenario."""
        self.run_yaml_scenario("test_data_loan_security.yaml")
