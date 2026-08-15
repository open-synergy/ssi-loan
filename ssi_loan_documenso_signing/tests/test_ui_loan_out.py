# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanOut(HttpSavepointCase):
    """Tour test for the ``loan.out`` Documenso signing delta."""

    def setUp(self):
        """Prepare accounts, a loan type, and one Waiting record.

        Pre-Condition IK (delta): a record already Waiting for
        Approval, whose active Approval Template has **no** Documenso
        Signing Template configured -- the Signature Requests tab is
        still shown (``_documenso_signing_create_page = True``), but
        base Flow steps 3-4 (Approve / OK) are unaffected, per this
        module's own Modified Flow bullet 2. ``admin`` is added to
        ``loan_out_validator_group`` (implies user + viewer groups) so
        it satisfies every policy field checked along the way,
        including being the sole approver on the default approval
        template -- same fixture shape as
        ``ssi_loan.tests.test_ui_loan_out``.

        Overrides ``setUp`` rather than ``setUpClass`` because
        ``HttpCase``/``TransactionCase`` only expose ``self.env``
        per-test (set up in ``setUp``); ``cls.env`` is never assigned
        at the class level.
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
                "code": "TOURLOD1",
                "name": "Tour Loan Out Documenso Realization Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_rounding = self.env["account.account"].create(
            {
                "code": "TOURLOD2",
                "name": "Tour Loan Out Documenso Rounding Account",
                "user_type_id": revenue_type.id,
            }
        )
        account_interest = self.env["account.account"].create(
            {
                "code": "TOURLOD3",
                "name": "Tour Loan Out Documenso Interest Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_interest_income = self.env["account.account"].create(
            {
                "code": "TOURLOD4",
                "name": "Tour Loan Out Documenso Interest Income Account",
                "user_type_id": revenue_type.id,
            }
        )
        account_principle_short = self.env["account.account"].create(
            {
                "code": "TOURLOD5",
                "name": "Tour Loan Out Documenso Short-Term Principle Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_principle_long = self.env["account.account"].create(
            {
                "code": "TOURLOD6",
                "name": "Tour Loan Out Documenso Long-Term Principle Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        realization_journal = self.env["account.journal"].create(
            {
                "name": "Tour Loan Out Documenso Realization Journal",
                "code": "TLODJ1",
                "type": "general",
            }
        )
        interest_journal = self.env["account.journal"].create(
            {
                "name": "Tour Loan Out Documenso Interest Journal",
                "code": "TLODJ2",
                "type": "general",
            }
        )
        self.loan_type = self.env["loan.type"].create(
            {
                "name": "Tour Loan Type Out Documenso",
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

        # Pre-Condition IK 05-approve.md (delta): record already
        # Waiting for Approval, with ``admin`` as its active approver,
        # and no Documenso Signing Template on the active Approval
        # Template.
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
        """Run the approve tour for the Documenso signing delta.

        IK: docs/loan_out/05-approve.md (E2a delta -- Modified Flow)
        """
        self.start_tour(
            "/web",
            "ssi_loan_documenso_signing_loan_out_approve",
            login="admin",
        )
