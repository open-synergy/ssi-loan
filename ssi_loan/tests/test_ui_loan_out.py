# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanOut(HttpCase):
    """Tour tests for the ``loan.out`` work instructions."""

    def setUp(self):
        """Prepare accounts, a loan type, and precondition records.

        Pre-Condition IK: every tour needs a fully-configured outgoing
        ``loan.type`` (realization/interest accounts and journals) so
        that ``action_compute_payment`` and ``action_approve_approval``
        (which posts the realization journal entry) can run. The
        ``confirm``/``approve``/``cancel`` tours also need a record
        already sitting in the state the IK's Flow starts from, built
        here via ORM calls rather than UI clicks. ``admin`` is added to
        ``loan_out_validator_group`` (implies user + viewer groups) so
        it satisfies every policy field checked along the way,
        including being the sole approver on the default approval
        template.

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
                "code": "TOURLO01",
                "name": "Tour Loan Out Realization Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_rounding = self.env["account.account"].create(
            {
                "code": "TOURLO02",
                "name": "Tour Loan Out Rounding Account",
                "user_type_id": revenue_type.id,
            }
        )
        account_interest = self.env["account.account"].create(
            {
                "code": "TOURLO03",
                "name": "Tour Loan Out Interest Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_interest_income = self.env["account.account"].create(
            {
                "code": "TOURLO04",
                "name": "Tour Loan Out Interest Income Account",
                "user_type_id": revenue_type.id,
            }
        )
        realization_journal = self.env["account.journal"].create(
            {
                "name": "Tour Loan Out Realization Journal",
                "code": "TLOJ1",
                "type": "general",
            }
        )
        interest_journal = self.env["account.journal"].create(
            {
                "name": "Tour Loan Out Interest Journal",
                "code": "TLOJ2",
                "type": "general",
            }
        )
        self.loan_type = self.env["loan.type"].create(
            {
                "name": "Tour Loan Type Out",
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
            }
        )
        self.cancel_reason = self.env["base.cancel_reason"].create(
            {
                "name": "Tour Cancel Reason",
                "code": "TOURX01",
                "global_use": True,
            }
        )

        # Pre-Condition IK 14-compute-payment-schedule.md: draft record
        # with Loan Type/Amount/Interest/Period/First Payment Date
        # already filled, schedule NOT computed yet.
        partner_schedule = self.env["res.partner"].create(
            {"name": "Tour Loan Out Schedule Partner"}
        )
        self.loan_out_schedule = self.env["loan.out"].create(
            self._loan_out_values(partner_schedule)
        )

        # Pre-Condition IK 04-confirm.md: draft record whose Total
        # Principle Amount already equals Loan Amount.
        partner_confirm = self.env["res.partner"].create(
            {"name": "Tour Loan Out Confirm Partner"}
        )
        self.loan_out_confirm = self.env["loan.out"].create(
            self._loan_out_values(partner_confirm)
        )
        self.loan_out_confirm.action_compute_payment()

        # Pre-Condition IK 05-approve.md: record already Waiting for
        # Approval, with ``admin`` as its active approver.
        partner_approve = self.env["res.partner"].create(
            {"name": "Tour Loan Out Approve Partner"}
        )
        self.loan_out_approve = self.env["loan.out"].create(
            self._loan_out_values(partner_approve)
        )
        self.loan_out_approve.action_compute_payment()
        self.loan_out_approve.with_context(bypass_policy_check=True).action_confirm()

        # Pre-Condition IK 10-cancel.md: a plain Draft record (cancel is
        # also allowed from Draft, so no schedule/confirm needed).
        partner_cancel = self.env["res.partner"].create(
            {"name": "Tour Loan Out Cancel Partner"}
        )
        self.loan_out_cancel = self.env["loan.out"].create(
            self._loan_out_values(partner_cancel)
        )

    def _loan_out_values(self, partner):
        """Build ``loan.out`` create values shared by the fixtures.

        :param partner: ``res.partner`` record to use as borrower
        :return: dict of field values for ``loan.out.create``
        """
        return {
            "date": "2024-01-01",
            "partner_id": partner.id,
            "type_id": self.loan_type.id,
            "currency_id": self.env.ref("base.USD").id,
            "loan_amount": 3000.0,
            "maximum_loan_amount": 6000.0,
            "interest": 3.0,
            "manual_loan_period": 6,
            "first_payment_date": "2024-02-01",
        }

    def test_create(self):
        """Run the create tour for ``loan.out``.

        IK: docs/loan_out/01-create.md
        """
        self.start_tour("/web", "ssi_loan_loan_out_create", login="admin")

    def test_compute_payment_schedule(self):
        """Run the compute payment schedule tour for ``loan.out``.

        IK: docs/loan_out/14-compute-payment-schedule.md
        """
        self.start_tour(
            "/web", "ssi_loan_loan_out_compute_payment_schedule", login="admin"
        )

    def test_confirm(self):
        """Run the confirm tour for ``loan.out``.

        IK: docs/loan_out/04-confirm.md
        """
        self.start_tour("/web", "ssi_loan_loan_out_confirm", login="admin")

    def test_approve(self):
        """Run the approve tour for ``loan.out``.

        IK: docs/loan_out/05-approve.md
        """
        self.start_tour("/web", "ssi_loan_loan_out_approve", login="admin")

    def test_cancel(self):
        """Run the cancel tour for ``loan.out``.

        IK: docs/loan_out/10-cancel.md
        """
        self.start_tour("/web", "ssi_loan_loan_out_cancel", login="admin")
