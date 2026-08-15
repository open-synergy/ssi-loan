# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanCollateralType(HttpSavepointCase):
    """Tour tests for the ``loan_collateral_type`` work instructions."""

    def setUp(self):
        """Create fixtures the edit/delete/deactivate/activate tours need.

        Creates one ``loan_collateral_type`` record per tour that acts
        on an existing record (edit/delete/deactivate), plus one
        already-archived record for the activate tour (Pre-Condition
        IK of ``02-edit.md``/``03-delete.md``/``04-deactivate.md``/
        ``05-activate.md``).

        Overrides ``setUp`` rather than ``setUpClass`` so each
        test method gets independent, freshly-created fixtures
        instead of state shared across the whole test class.
        """
        super().setUp()
        loan_collateral_type_model = self.env["loan_collateral_type"]
        self.loan_collateral_type_edit = loan_collateral_type_model.create(
            {
                "name": "TOUR Loan Collateral Type Edit",
                "code": "/",
            }
        )
        self.loan_collateral_type_delete = loan_collateral_type_model.create(
            {
                "name": "TOUR Loan Collateral Type Delete",
                "code": "/",
            }
        )
        self.loan_collateral_type_deactivate = loan_collateral_type_model.create(
            {
                "name": "TOUR Loan Collateral Type Deactivate",
                "code": "/",
            }
        )
        self.loan_collateral_type_activate = loan_collateral_type_model.create(
            {
                "name": "TOUR Loan Collateral Type Activate",
                "code": "/",
                "active": False,
            }
        )

    def test_create(self):
        """Run the create tour for ``loan_collateral_type``.

        IK: docs/loan_collateral_type/01-create.md
        """
        self.start_tour("/web", "ssi_loan_loan_collateral_type_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``loan_collateral_type``.

        IK: docs/loan_collateral_type/02-edit.md
        """
        self.start_tour("/web", "ssi_loan_loan_collateral_type_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``loan_collateral_type``.

        IK: docs/loan_collateral_type/03-delete.md
        """
        self.start_tour("/web", "ssi_loan_loan_collateral_type_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``loan_collateral_type``.

        IK: docs/loan_collateral_type/04-deactivate.md
        """
        self.start_tour(
            "/web", "ssi_loan_loan_collateral_type_deactivate", login="admin"
        )

    def test_activate(self):
        """Run the activate tour for ``loan_collateral_type``.

        IK: docs/loan_collateral_type/05-activate.md
        """
        self.start_tour("/web", "ssi_loan_loan_collateral_type_activate", login="admin")
