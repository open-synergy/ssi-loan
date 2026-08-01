# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanIn(HttpCase):
    """Tour tests for the ``loan.in`` work instructions."""

    def setUp(self):
        """Prepare accounts, a loan type, and precondition records.

        Pre-Condition IK: every tour needs a fully-configured incoming
        ``loan.type`` (realization/interest/short- and long-term
        principle accounts and journals) so that
        ``action_compute_payment`` and ``action_approve_approval``
        (which posts the realization journal entry) can run. The
        ``confirm``/``approve``/``cancel`` tours also need a record
        already sitting in the state the IK's Flow starts from, built
        here via ORM calls rather than UI clicks. ``admin`` is added to
        ``loan_in_validator_group`` (implies user + viewer groups) so
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
            {"groups_id": [(4, self.env.ref("ssi_loan.loan_in_validator_group").id)]}
        )

        receivable_type = self.env.ref("account.data_account_type_receivable")
        revenue_type = self.env.ref("account.data_account_type_revenue")
        account_realization = self.env["account.account"].create(
            {
                "code": "TOURLI01",
                "name": "Tour Loan In Realization Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_rounding = self.env["account.account"].create(
            {
                "code": "TOURLI02",
                "name": "Tour Loan In Rounding Account",
                "user_type_id": revenue_type.id,
            }
        )
        account_interest = self.env["account.account"].create(
            {
                "code": "TOURLI03",
                "name": "Tour Loan In Interest Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_interest_income = self.env["account.account"].create(
            {
                "code": "TOURLI04",
                "name": "Tour Loan In Interest Income Account",
                "user_type_id": revenue_type.id,
            }
        )
        account_principle_short = self.env["account.account"].create(
            {
                "code": "TOURLI05",
                "name": "Tour Loan In Short-Term Principle Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_principle_long = self.env["account.account"].create(
            {
                "code": "TOURLI06",
                "name": "Tour Loan In Long-Term Principle Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        realization_journal = self.env["account.journal"].create(
            {
                "name": "Tour Loan In Realization Journal",
                "code": "TLIJ1",
                "type": "general",
            }
        )
        interest_journal = self.env["account.journal"].create(
            {
                "name": "Tour Loan In Interest Journal",
                "code": "TLIJ2",
                "type": "general",
            }
        )
        self.loan_type = self.env["loan.type"].create(
            {
                "name": "Tour Loan Type In",
                "code": "/",
                "direction": "in",
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
        self.cancel_reason = self.env["base.cancel_reason"].create(
            {
                "name": "Tour Cancel Reason In",
                "code": "TOURX02",
                "global_use": True,
            }
        )

        # Pre-Condition IK 14-compute-payment-schedule.md: draft record
        # with Loan Type/Amount/Interest/Period/First Payment Date
        # already filled, schedule NOT computed yet.
        partner_schedule = self.env["res.partner"].create(
            {"name": "Tour Loan In Schedule Partner"}
        )
        self.loan_in_schedule = self.env["loan.in"].create(
            self._loan_in_values(partner_schedule)
        )

        # Pre-Condition IK 04-confirm.md: draft record whose Total
        # Principle Amount already equals Loan Amount.
        partner_confirm = self.env["res.partner"].create(
            {"name": "Tour Loan In Confirm Partner"}
        )
        self.loan_in_confirm = self.env["loan.in"].create(
            self._loan_in_values(partner_confirm)
        )
        self.loan_in_confirm.action_compute_payment()

        # Pre-Condition IK 05-approve.md: record already Waiting for
        # Approval, with ``admin`` as its active approver.
        partner_approve = self.env["res.partner"].create(
            {"name": "Tour Loan In Approve Partner"}
        )
        self.loan_in_approve = self.env["loan.in"].create(
            self._loan_in_values(partner_approve)
        )
        self.loan_in_approve.action_compute_payment()
        self.loan_in_approve.with_context(bypass_policy_check=True).action_confirm()

        # Pre-Condition IK 10-cancel.md: a plain Draft record (cancel is
        # also allowed from Draft, so no schedule/confirm needed).
        partner_cancel = self.env["res.partner"].create(
            {"name": "Tour Loan In Cancel Partner"}
        )
        self.loan_in_cancel = self.env["loan.in"].create(
            self._loan_in_values(partner_cancel)
        )

    def _loan_in_values(self, partner):
        """Build ``loan.in`` create values shared by the fixtures.

        ``user_id`` is forced to ``admin`` because ``loan_in_internal_
        user_rule`` only lets a user see records where ``user_id`` is
        themselves; records created here run under ``self.env``'s
        default user, not the ``admin`` who logs into the tour, so the
        list would otherwise render empty for the tour user.

        :param partner: ``res.partner`` record to use as lender
        :return: dict of field values for ``loan.in.create``
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
            "user_id": self.env.ref("base.user_admin").id,
        }

    def test_create(self):
        """Run the create tour for ``loan.in``.

        IK: docs/loan_in/01-create.md
        """
        self.start_tour("/web", "ssi_loan_loan_in_create", login="admin")

    def test_compute_payment_schedule(self):
        """Run the compute payment schedule tour for ``loan.in``.

        IK: docs/loan_in/14-compute-payment-schedule.md
        """
        self.start_tour(
            "/web", "ssi_loan_loan_in_compute_payment_schedule", login="admin"
        )

    def test_confirm(self):
        """Run the confirm tour for ``loan.in``.

        IK: docs/loan_in/04-confirm.md
        """
        self.start_tour("/web", "ssi_loan_loan_in_confirm", login="admin")

    def test_approve(self):
        """Run the approve tour for ``loan.in``.

        IK: docs/loan_in/05-approve.md
        """
        self.start_tour("/web", "ssi_loan_loan_in_approve", login="admin")

    def test_cancel(self):
        """Run the cancel tour for ``loan.in``.

        IK: docs/loan_in/10-cancel.md
        """
        self.start_tour("/web", "ssi_loan_loan_in_cancel", login="admin")
