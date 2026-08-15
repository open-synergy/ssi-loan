# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanOut(HttpSavepointCase):
    """Tour test for the Operating Unit field on ``loan.out`` create."""

    def setUp(self):
        """Grant ``admin`` the multi operating unit group.

        Pre-Condition IK: the Operating Unit field is gated by
        ``groups="operating_unit.group_multi_operating_unit"`` in the
        form view -- without membership, the field is never rendered
        and the delta assertion would never find it. ``admin`` also
        needs at least one operating unit assigned so the field has a
        meaningful (non-empty) allowed set.

        Overrides ``setUp`` rather than ``setUpClass`` because
        ``HttpCase``/``TransactionCase`` only expose ``self.env``
        per-test (set up in ``setUp``); ``cls.env`` is never assigned
        at the class level (same pattern as
        ``ssi_loan/tests/test_ui_loan_out.py``).
        """
        super().setUp()
        self.user_admin = self.env.ref("base.user_admin")
        operating_unit_partner = self.env["res.partner"].create(
            {"name": "Tour Loan Out OU Partner"}
        )
        self.operating_unit = self.env["operating.unit"].create(
            {
                "name": "Tour Loan Out Operating Unit",
                "code": "TLOOU",
                "partner_id": operating_unit_partner.id,
            }
        )
        self.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, self.user_admin.id)]}
        )
        self.user_admin.sudo().write(
            {
                "assigned_operating_unit_ids": [(4, self.operating_unit.id)],
                "default_operating_unit_id": self.operating_unit.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``loan.out``.

        IK: docs/loan_out/01-create.md (E1 delta -- Additional Fields)
        """
        self.start_tour(
            "/web", "ssi_loan_operating_unit_loan_out_create", login="admin"
        )
