# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanAdditionalItem(HttpCase):
    """Tour tests for the ``loan.additional_item`` work instructions."""

    def setUp(self):
        """Create fixtures the edit/delete/deactivate/activate tours need.

        Creates one ``loan.additional_item`` record per tour that acts
        on an existing record (edit/delete/deactivate), plus one
        already-archived record for the activate tour (Pre-Condition
        IK of ``02-edit.md``/``03-delete.md``/``04-deactivate.md``/
        ``05-activate.md``).

        Overrides ``setUp`` rather than ``setUpClass`` because
        ``HttpCase``/``TransactionCase`` only expose ``self.env``
        per-test (set up in ``setUp``); ``cls.env`` is never assigned
        at the class level.
        """
        super().setUp()
        loan_additional_item_model = self.env["loan.additional_item"]
        self.loan_additional_item_edit = loan_additional_item_model.create(
            {
                "name": "TOUR Loan Additional Item Edit",
                "code": "/",
            }
        )
        self.loan_additional_item_delete = loan_additional_item_model.create(
            {
                "name": "TOUR Loan Additional Item Delete",
                "code": "/",
            }
        )
        self.loan_additional_item_deactivate = loan_additional_item_model.create(
            {
                "name": "TOUR Loan Additional Item Deactivate",
                "code": "/",
            }
        )
        self.loan_additional_item_activate = loan_additional_item_model.create(
            {
                "name": "TOUR Loan Additional Item Activate",
                "code": "/",
                "active": False,
            }
        )

    def test_create(self):
        """Run the create tour for ``loan.additional_item``.

        IK: docs/loan_additional_item/01-create.md
        """
        self.start_tour("/web", "ssi_loan_loan_additional_item_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``loan.additional_item``.

        IK: docs/loan_additional_item/02-edit.md
        """
        self.start_tour("/web", "ssi_loan_loan_additional_item_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``loan.additional_item``.

        IK: docs/loan_additional_item/03-delete.md
        """
        self.start_tour("/web", "ssi_loan_loan_additional_item_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``loan.additional_item``.

        IK: docs/loan_additional_item/04-deactivate.md
        """
        self.start_tour(
            "/web", "ssi_loan_loan_additional_item_deactivate", login="admin"
        )

    def test_activate(self):
        """Run the activate tour for ``loan.additional_item``.

        IK: docs/loan_additional_item/05-activate.md
        """
        self.start_tour("/web", "ssi_loan_loan_additional_item_activate", login="admin")
