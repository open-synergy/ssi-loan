# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanType(HttpCase):
    """Tour tests for the ``loan.type`` work instructions."""

    def setUp(self):
        """Activate the currency required by the create tour.

        Pre-Condition IK: the Currency field must offer a
        selectable option. ``base.USD`` always exists but may be
        inactive depending on the database's default company
        currency, so force it active instead of assuming the
        demo state.

        Overrides ``setUp`` rather than ``setUpClass`` because
        ``HttpCase``/``TransactionCase`` only expose ``self.env``
        per-test (set up in ``setUp``); ``cls.env`` is never
        assigned at the class level.
        """
        super().setUp()
        self.env.ref("base.USD").sudo().write({"active": True})

    def test_create(self):
        """Run the create tour for ``loan.type``.

        IK: docs/loan_type/01-create.md
        """
        self.start_tour("/web", "ssi_loan_loan_type_create", login="admin")
