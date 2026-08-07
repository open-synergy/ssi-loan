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

        # Pre-Condition IK 02-edit.md: a plain Draft record whose
        # fields can be changed and re-saved.
        partner_edit = self.env["res.partner"].create(
            {"name": "Tour Loan In Edit Partner"}
        )
        self.loan_in_edit = self.env["loan.in"].create(
            self._loan_in_values(partner_edit)
        )

        # Pre-Condition IK 03-delete.md: a plain Draft record whose
        # document number is still "/" (delete is also allowed from
        # Draft with an unassigned number).
        partner_delete = self.env["res.partner"].create(
            {"name": "Tour Loan In Delete Partner"}
        )
        self.loan_in_delete = self.env["loan.in"].create(
            self._loan_in_values(partner_delete)
        )

        # Pre-Condition IK 06-reject.md: record already Waiting for
        # Approval, with ``admin`` as its active approver.
        partner_reject = self.env["res.partner"].create(
            {"name": "Tour Loan In Reject Partner"}
        )
        self.loan_in_reject = self.env["loan.in"].create(
            self._loan_in_values(partner_reject)
        )
        self.loan_in_reject.action_compute_payment()
        self.loan_in_reject.with_context(bypass_policy_check=True).action_confirm()

        # Pre-Condition IK 12-restart.md: a Rejected record (restart
        # is also allowed from Cancelled). ``action_reject_approval``
        # only transitions the record's state through the multiple
        # approval workflow (``mixin.multiple_approval._action_
        # approval``), which is sensitive to the exact acting-user/
        # approval-instance setup. Since this fixture only needs the
        # record to *sit* in Rejected status (the tour itself is what
        # exercises the Restart button), the state is written directly
        # instead of driving the full approval mechanism.
        partner_restart = self.env["res.partner"].create(
            {"name": "Tour Loan In Restart Partner"}
        )
        self.loan_in_restart = self.env["loan.in"].create(
            self._loan_in_values(partner_restart)
        )
        self.loan_in_restart.action_compute_payment()
        self.loan_in_restart.with_context(bypass_policy_check=True).action_confirm()
        self.loan_in_restart.sudo().write({"state": "reject"})

        # Pre-Condition IK 13-reset-number.md: a Draft record whose
        # document number was already assigned (simulating a record
        # that reached Ready to Process, where it received a number,
        # and was later cancelled and restarted back to Draft, which
        # keeps the assigned number).
        partner_reset_number = self.env["res.partner"].create(
            {"name": "Tour Loan In Reset Number Partner"}
        )
        self.loan_in_reset_number = self.env["loan.in"].create(
            self._loan_in_values(partner_reset_number)
        )
        self.loan_in_reset_number.sudo().write({"name": "TOUR-LI-RESET-0001"})

        # Pre-Condition IK 15-mark-principle-as-manual.md: a Draft
        # record with a freshly computed schedule (each line's
        # Principle Payment State defaults to Unpaid, not yet
        # Manually Control).
        partner_mark = self.env["res.partner"].create(
            {"name": "Tour Loan In Mark Partner"}
        )
        self.loan_in_mark = self.env["loan.in"].create(
            self._loan_in_values(partner_mark)
        )
        self.loan_in_mark.action_compute_payment()

        # Pre-Condition IK 16-unmark-principle-as-manual.md: a Draft
        # record whose first schedule line is already Manually
        # Control. Written directly (rather than via
        # ``action_mark_principle_as_manual``) since this fixture only
        # needs the line to already sit in that state; the tour itself
        # is what exercises the Unmark button.
        partner_unmark = self.env["res.partner"].create(
            {"name": "Tour Loan In Unmark Partner"}
        )
        self.loan_in_unmark = self.env["loan.in"].create(
            self._loan_in_values(partner_unmark)
        )
        self.loan_in_unmark.action_compute_payment()
        self.loan_in_unmark.payment_schedule_ids[:1].sudo().write(
            {"principle_payment_state": "manual"}
        )

        # Pre-Condition IK 17-realize-interest.md: an In Progress
        # record whose first schedule line's Interest Payment State
        # is still Unrealized. ``action_approve_approval`` only marks
        # the approval done when the ACTING user is a registered
        # approver, hence ``with_user(admin)`` (see 12-restart.md
        # fixture above). ``state`` is then forced to ``open`` directly
        # because the Ready-to-Process-to-In-Progress transition is a
        # base.automation triggered by bank reconciliation
        # (docs/loan_in/07-start.md), out of scope for this tour.
        partner_realize = self.env["res.partner"].create(
            {"name": "Tour Loan In Realize Partner"}
        )
        self.loan_in_realize = self.env["loan.in"].create(
            self._loan_in_values(partner_realize)
        )
        self.loan_in_realize.action_compute_payment()
        self.loan_in_realize.with_context(bypass_policy_check=True).action_confirm()
        self.loan_in_realize.with_user(self.env.ref("base.user_admin")).with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        self.loan_in_realize.sudo().write({"state": "open"})

        # Pre-Condition IK 18-unrealize-interest.md: same as above,
        # but the first schedule line's interest is already realized
        # (Interest Payment State is Unpaid).
        partner_unrealize = self.env["res.partner"].create(
            {"name": "Tour Loan In Unrealize Partner"}
        )
        self.loan_in_unrealize = self.env["loan.in"].create(
            self._loan_in_values(partner_unrealize)
        )
        self.loan_in_unrealize.action_compute_payment()
        self.loan_in_unrealize.with_context(bypass_policy_check=True).action_confirm()
        self.loan_in_unrealize.with_user(self.env.ref("base.user_admin")).with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        self.loan_in_unrealize.sudo().write({"state": "open"})
        self.loan_in_unrealize.payment_schedule_ids[:1].action_realize_interest()

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

    def test_edit(self):
        """Run the edit tour for ``loan.in``.

        IK: docs/loan_in/02-edit.md
        """
        self.start_tour("/web", "ssi_loan_loan_in_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``loan.in``.

        IK: docs/loan_in/03-delete.md
        """
        self.start_tour("/web", "ssi_loan_loan_in_delete", login="admin")

    def test_reject(self):
        """Run the reject tour for ``loan.in``.

        IK: docs/loan_in/06-reject.md
        """
        self.start_tour("/web", "ssi_loan_loan_in_reject", login="admin")

    def test_restart(self):
        """Run the restart tour for ``loan.in``.

        IK: docs/loan_in/12-restart.md
        """
        self.start_tour("/web", "ssi_loan_loan_in_restart", login="admin")

    def test_reset_number(self):
        """Run the reset document number tour for ``loan.in``.

        IK: docs/loan_in/13-reset-number.md
        """
        self.start_tour("/web", "ssi_loan_loan_in_reset_number", login="admin")

    def test_mark_principle_as_manual(self):
        """Run the mark principle as manual tour for ``loan.in``.

        IK: docs/loan_in/15-mark-principle-as-manual.md
        """
        self.start_tour(
            "/web", "ssi_loan_loan_in_mark_principle_as_manual", login="admin"
        )

    def test_unmark_principle_as_manual(self):
        """Run the unmark principle as manual tour for ``loan.in``.

        IK: docs/loan_in/16-unmark-principle-as-manual.md
        """
        self.start_tour(
            "/web", "ssi_loan_loan_in_unmark_principle_as_manual", login="admin"
        )

    def test_realize_interest(self):
        """Run the realize interest tour for ``loan.in``.

        IK: docs/loan_in/17-realize-interest.md
        """
        self.start_tour("/web", "ssi_loan_loan_in_realize_interest", login="admin")

    def test_unrealize_interest(self):
        """Run the unrealize interest tour for ``loan.in``.

        IK: docs/loan_in/18-unrealize-interest.md
        """
        self.start_tour("/web", "ssi_loan_loan_in_unrealize_interest", login="admin")
