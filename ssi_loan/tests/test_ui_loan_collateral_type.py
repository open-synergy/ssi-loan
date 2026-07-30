# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanCollateralType(HttpCase):
    """Tour tests for the ``loan_collateral_type`` work instructions."""

    def test_create(self):
        """Run the create tour for ``loan_collateral_type``.

        IK: docs/loan_collateral_type/01-create.md
        """
        self.start_tour(
            "/web", "ssi_loan_loan_collateral_type_create", login="admin"
        )
