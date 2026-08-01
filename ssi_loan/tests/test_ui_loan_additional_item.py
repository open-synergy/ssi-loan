# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanAdditionalItem(HttpCase):
    """Tour tests for the ``loan.additional_item`` work instructions."""

    def test_create(self):
        """Run the create tour for ``loan.additional_item``.

        IK: docs/loan_additional_item/01-create.md
        """
        self.start_tour("/web", "ssi_loan_loan_additional_item_create", login="admin")
