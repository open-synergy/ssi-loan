# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanOut(HttpCase):
    """Tour test for the ``loan.out`` Documenso signing delta."""

    def setUp(self):
        """Prepare accounts, a loan type, and the approve fixture.

        Pre-Condition IK: the approve tour needs a fully-configured
        outgoing ``loan.type`` (realization/interest/short- and
        long-term principle accounts and journals) so that
        ``action_compute_payment`` and ``action_approve_approval``
        (which posts the realization journal entry) can run, and a
        record already sitting in **Waiting for Approval**, built here
        via ORM calls rather than UI clicks. ``admin`` is added to
        ``loan_out_validator_group`` so it satisfies every policy field
        checked along the way. The fixture's approval template is left
        without a Documenso Signing Template configured, so the base
        Approve/OK Flow still applies (Keputusan Desain, issue
        open-synergy/ssi-loan#32) and the tour does not need to reach
        the external Documenso server.

        Overrides ``setUp`` rather than ``setUpClass`` because
        ``HttpCase``/``TransactionCase`` only expose ``self.env``
        per-test (set up in ``setUp``); ``cls.env`` is never assigned
        at the class level (same pattern as
        ``ssi_loan/tests/test_ui_loan_out.py``).
        """
        super().setUp()
        self.env.ref("base.USD").sudo().write({"active": True})
        self.env.ref("base.user_admin").sudo().write(
            {"groups_id": [(4, self.env.ref("ssi_loan.loan_out_validator_group").id)]}
        )

        receivable_type = self.env.ref("account.data_account_type_receivable")
        revenue_type = self.env.ref("account.data_account_type_revenue")
        account_realization = self.env["account.account"].create(
            {
                "code": "TDSLO01",
                "name": "Tour Documenso Loan Out Realization Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_rounding = self.env["account.account"].create(
            {
                "code": "TDSLO02",
                "name": "Tour Documenso Loan Out Rounding Account",
                "user_type_id": revenue_type.id,
            }
        )
        account_interest = self.env["account.account"].create(
            {
                "code": "TDSLO03",
                "name": "Tour Documenso Loan Out Interest Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_interest_income = self.env["account.account"].create(
            {
                "code": "TDSLO04",
                "name": "Tour Documenso Loan Out Interest Income Account",
                "user_type_id": revenue_type.id,
            }
        )
        account_principle_short = self.env["account.account"].create(
            {
                "code": "TDSLO05",
                "name": "Tour Documenso Loan Out Short-Term Principle Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_principle_long = self.env["account.account"].create(
            {
                "code": "TDSLO06",
                "name": "Tour Documenso Loan Out Long-Term Principle Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        realization_journal = self.env["account.journal"].create(
            {
                "name": "Tour Documenso Loan Out Realization Journal",
                "code": "TDLOJ1",
                "type": "general",
            }
        )
        interest_journal = self.env["account.journal"].create(
            {
                "name": "Tour Documenso Loan Out Interest Journal",
                "code": "TDLOJ2",
                "type": "general",
            }
        )
        self.loan_type = self.env["loan.type"].create(
            {
                "name": "Tour Documenso Loan Type Out",
                "code": "/",
                "direction": "out",
                "interest_method": "flat",
                "currency_id": self.env.ref("base.USD").id,
                "interest_amount": 3.0,
                "maximum_loan_amount": 6000.0,
                "maximum_installment_period": 12,
                "realization_journal_id": realization_journal.id,
                "account_realization_id": account_realization.id,
                "account_rounding_id": account_rounding.id,
                "interest_journal_id": interest_journal.id,
                "account_interest_id": account_interest.id,
                "account_interest_income_id": account_interest_income.id,
                "short_account_principle_id": account_principle_short.id,
                "long_account_principle_id": account_principle_long.id,
            }
        )

        # Pre-Condition IK 05-approve.md (delta): record already Waiting
        # for Approval, with ``admin`` as its active approver, and no
        # Documenso Signing Template configured on the approval template.
        partner_approve = self.env["res.partner"].create(
            {"name": "Tour Loan Out Documenso Approve Partner"}
        )
        self.loan_out_approve = self.env["loan.out"].create(
            {
                "date": "2024-01-01",
                "partner_id": partner_approve.id,
                "type_id": self.loan_type.id,
                "currency_id": self.env.ref("base.USD").id,
                "loan_amount": 3000.0,
                "maximum_loan_amount": 6000.0,
                "interest": 3.0,
                "manual_loan_period": 6,
                "first_payment_date": "2024-02-01",
                "user_id": self.env.ref("base.user_admin").id,
            }
        )
        self.loan_out_approve.action_compute_payment()
        self.loan_out_approve.with_context(bypass_policy_check=True).action_confirm()

    def test_approve(self):
        """Run the approve tour for the ``loan.out`` Documenso delta.

        IK: docs/loan_out/05-approve.md (E2a delta -- Modified Flow)
        """
        self.start_tour(
            "/web", "ssi_loan_documenso_signing_loan_out_approve", login="admin"
        )
