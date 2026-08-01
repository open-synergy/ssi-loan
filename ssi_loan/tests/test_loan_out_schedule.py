# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestLoanOutSchedule(YamlTransactionCase):
    """Cover ``loan.payment_schedule_out`` action methods and computes.

    Exercises ``action_mark_principle_as_manual``,
    ``action_unmark_principle_as_manual``, ``action_realize_interest``,
    and ``action_unrealize_interest``, the ``installment_amount`` and
    ``additional_amount`` computes, and the
    ``_check_interest_realization_move`` cancellation gate.
    """

    def test_loan_out_schedule(self):
        """Run the ``test_data_loan_out_schedule.yaml`` scenario."""
        self.run_yaml_scenario("test_data_loan_out_schedule.yaml")
