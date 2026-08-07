# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanType(HttpCase):
    """Tour tests for the ``loan.type`` work instructions."""

    def setUp(self):
        """Activate the currency and create fixtures the tours need.

        Pre-Condition IK: the Currency field must offer a
        selectable option. ``base.USD`` always exists but may be
        inactive depending on the database's default company
        currency, so force it active instead of assuming the
        demo state.

        Also creates one ``loan.type`` record per tour that acts on
        an existing record (edit/delete/deactivate), plus one
        already-archived record for the activate tour
        (Pre-Condition IK of ``02-edit.md``/``03-delete.md``/
        ``04-deactivate.md``/``05-activate.md``).

        Overrides ``setUp`` rather than ``setUpClass`` because
        ``HttpCase``/``TransactionCase`` only expose ``self.env``
        per-test (set up in ``setUp``); ``cls.env`` is never
        assigned at the class level.
        """
        super().setUp()
        currency = self.env.ref("base.USD")
        currency.sudo().write({"active": True})
        loan_type_model = self.env["loan.type"]
        self.loan_type_edit = loan_type_model.create(
            {
                "name": "TOUR Loan Type Edit",
                "code": "/",
                "direction": "out",
                "currency_id": currency.id,
                "maximum_loan_amount": 100000000,
            }
        )
        self.loan_type_delete = loan_type_model.create(
            {
                "name": "TOUR Loan Type Delete",
                "code": "/",
                "direction": "out",
                "currency_id": currency.id,
                "maximum_loan_amount": 100000000,
            }
        )
        self.loan_type_deactivate = loan_type_model.create(
            {
                "name": "TOUR Loan Type Deactivate",
                "code": "/",
                "direction": "out",
                "currency_id": currency.id,
                "maximum_loan_amount": 100000000,
            }
        )
        self.loan_type_activate = loan_type_model.create(
            {
                "name": "TOUR Loan Type Activate",
                "code": "/",
                "direction": "out",
                "currency_id": currency.id,
                "maximum_loan_amount": 100000000,
                "active": False,
            }
        )

    def test_create(self):
        """Run the create tour for ``loan.type``.

        IK: docs/loan_type/01-create.md
        """
        self.start_tour("/web", "ssi_loan_loan_type_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``loan.type``.

        IK: docs/loan_type/02-edit.md
        """
        self.start_tour("/web", "ssi_loan_loan_type_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``loan.type``.

        IK: docs/loan_type/03-delete.md
        """
        self.start_tour("/web", "ssi_loan_loan_type_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``loan.type``.

        IK: docs/loan_type/04-deactivate.md
        """
        self.start_tour("/web", "ssi_loan_loan_type_deactivate", login="admin")

    def test_activate(self):
        """Run the activate tour for ``loan.type``.

        IK: docs/loan_type/05-activate.md
        """
        self.start_tour("/web", "ssi_loan_loan_type_activate", login="admin")
