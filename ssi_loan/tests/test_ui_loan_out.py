# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanOut(HttpSavepointCase):
    """Tour tests for the ``loan.out`` work instructions."""

    def setUp(self):
        """Prepare accounts, a loan type, and precondition records.

        Pre-Condition IK: every tour needs a fully-configured outgoing
        ``loan.type`` (realization/interest/short- and long-term
        principle accounts and journals) so that
        ``action_compute_payment`` and ``action_approve_approval``
        (which posts the realization journal entry) can run. The
        ``confirm``/``approve``/``cancel`` tours also need a record
        already sitting in the state the IK's Flow starts from, built
        here via ORM calls rather than UI clicks. ``admin`` is added to
        ``loan_out_validator_group`` (implies user + viewer groups) so
        it satisfies every policy field checked along the way,
        including being the sole approver on the default approval
        template.

        Overrides ``setUp`` rather than ``setUpClass`` so each
        test method gets independent, freshly-created fixtures
        instead of state shared across the whole test class.
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
        account_principle_short = self.env["account.account"].create(
            {
                "code": "TOURLO05",
                "name": "Tour Loan Out Short-Term Principle Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_principle_long = self.env["account.account"].create(
            {
                "code": "TOURLO06",
                "name": "Tour Loan Out Long-Term Principle Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
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
                "short_account_principle_id": account_principle_short.id,
                "long_account_principle_id": account_principle_long.id,
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

        # Pre-Condition IK 02-edit.md: a plain Draft record whose
        # fields can be changed and re-saved.
        partner_edit = self.env["res.partner"].create(
            {"name": "Tour Loan Out Edit Partner"}
        )
        self.loan_out_edit = self.env["loan.out"].create(
            self._loan_out_values(partner_edit)
        )

        # Pre-Condition IK 03-delete.md: a plain Draft record whose
        # document number is still "/" (delete is also allowed from
        # Draft with an unassigned number).
        partner_delete = self.env["res.partner"].create(
            {"name": "Tour Loan Out Delete Partner"}
        )
        self.loan_out_delete = self.env["loan.out"].create(
            self._loan_out_values(partner_delete)
        )

        # Pre-Condition IK 06-reject.md: record already Waiting for
        # Approval, with ``admin`` as its active approver.
        partner_reject = self.env["res.partner"].create(
            {"name": "Tour Loan Out Reject Partner"}
        )
        self.loan_out_reject = self.env["loan.out"].create(
            self._loan_out_values(partner_reject)
        )
        self.loan_out_reject.action_compute_payment()
        self.loan_out_reject.with_context(bypass_policy_check=True).action_confirm()

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
            {"name": "Tour Loan Out Restart Partner"}
        )
        self.loan_out_restart = self.env["loan.out"].create(
            self._loan_out_values(partner_restart)
        )
        self.loan_out_restart.action_compute_payment()
        self.loan_out_restart.with_context(bypass_policy_check=True).action_confirm()
        self.loan_out_restart.sudo().write({"state": "reject"})

        # Pre-Condition IK 13-reset-number.md: a Draft record whose
        # document number was already assigned (simulating a record
        # that reached Ready to Process, where it received a number,
        # and was later cancelled and restarted back to Draft, which
        # keeps the assigned number).
        partner_reset_number = self.env["res.partner"].create(
            {"name": "Tour Loan Out Reset Number Partner"}
        )
        self.loan_out_reset_number = self.env["loan.out"].create(
            self._loan_out_values(partner_reset_number)
        )
        self.loan_out_reset_number.sudo().write({"name": "TOUR-LO-RESET-0001"})

        # Pre-Condition IK 15-mark-principle-as-manual.md: a Draft
        # record with a freshly computed schedule (each line's
        # Principle Payment State defaults to Unpaid, not yet
        # Manually Control).
        partner_mark = self.env["res.partner"].create(
            {"name": "Tour Loan Out Mark Partner"}
        )
        self.loan_out_mark = self.env["loan.out"].create(
            self._loan_out_values(partner_mark)
        )
        self.loan_out_mark.action_compute_payment()

        # Pre-Condition IK 16-unmark-principle-as-manual.md: a Draft
        # record with a freshly computed schedule. The line's
        # Principle Payment State is not marked Manually Control here
        # in Python: it is a computed, readonly field
        # (``loan.payment_schedule_mixin._compute_state``), and the
        # ``ssi_loan_loan_out_unmark_principle_as_manual`` tour instead
        # drives the Mark button live as a guard step before exercising
        # Unmark (see ``static/tests/tours/loan_out_tour.js``).
        partner_unmark = self.env["res.partner"].create(
            {"name": "Tour Loan Out Unmark Partner"}
        )
        self.loan_out_unmark = self.env["loan.out"].create(
            self._loan_out_values(partner_unmark)
        )
        self.loan_out_unmark.action_compute_payment()

        # Pre-Condition IK 17-realize-interest.md: an In Progress
        # record whose first schedule line's Interest Payment State
        # is still Unrealized. ``action_approve_approval`` only marks
        # the approval done when the ACTING user is a registered
        # approver, hence ``with_user(admin)`` (see 12-restart.md
        # fixture above). ``state`` is then forced to ``open`` directly
        # because the Ready-to-Process-to-In-Progress transition is a
        # base.automation triggered by bank reconciliation
        # (docs/loan_out/07-start.md), out of scope for this tour.
        partner_realize = self.env["res.partner"].create(
            {"name": "Tour Loan Out Realize Partner"}
        )
        self.loan_out_realize = self.env["loan.out"].create(
            self._loan_out_values(partner_realize)
        )
        self.loan_out_realize.action_compute_payment()
        self.loan_out_realize.with_context(bypass_policy_check=True).action_confirm()
        self.loan_out_realize.with_user(self.env.ref("base.user_admin")).with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        self.loan_out_realize.sudo().write({"state": "open"})

        # Pre-Condition IK 18-unrealize-interest.md: same as above,
        # but the first schedule line's interest is already realized
        # (Interest Payment State is Unpaid).
        partner_unrealize = self.env["res.partner"].create(
            {"name": "Tour Loan Out Unrealize Partner"}
        )
        self.loan_out_unrealize = self.env["loan.out"].create(
            self._loan_out_values(partner_unrealize)
        )
        self.loan_out_unrealize.action_compute_payment()
        self.loan_out_unrealize.with_context(bypass_policy_check=True).action_confirm()
        self.loan_out_unrealize.with_user(self.env.ref("base.user_admin")).with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        self.loan_out_unrealize.sudo().write({"state": "open"})
        self.loan_out_unrealize.payment_schedule_ids[:1].action_realize_interest()

    def _loan_out_values(self, partner):
        """Build ``loan.out`` create values shared by the fixtures.

        ``user_id`` is forced to ``admin`` because ``loan_out_internal_
        user_rule`` only lets a user see records where ``user_id`` is
        themselves; records created here run under ``self.env``'s
        default user, not the ``admin`` who logs into the tour, so the
        list would otherwise render empty for the tour user.

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
            "user_id": self.env.ref("base.user_admin").id,
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

    def test_edit(self):
        """Run the edit tour for ``loan.out``.

        IK: docs/loan_out/02-edit.md
        """
        self.start_tour("/web", "ssi_loan_loan_out_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``loan.out``.

        IK: docs/loan_out/03-delete.md
        """
        self.start_tour("/web", "ssi_loan_loan_out_delete", login="admin")

    def test_reject(self):
        """Run the reject tour for ``loan.out``.

        IK: docs/loan_out/06-reject.md
        """
        self.start_tour("/web", "ssi_loan_loan_out_reject", login="admin")

    def test_restart(self):
        """Run the restart tour for ``loan.out``.

        IK: docs/loan_out/12-restart.md
        """
        self.start_tour("/web", "ssi_loan_loan_out_restart", login="admin")

    def test_reset_number(self):
        """Run the reset document number tour for ``loan.out``.

        IK: docs/loan_out/13-reset-number.md
        """
        self.start_tour("/web", "ssi_loan_loan_out_reset_number", login="admin")

    def test_mark_principle_as_manual(self):
        """Run the mark principle as manual tour for ``loan.out``.

        IK: docs/loan_out/15-mark-principle-as-manual.md
        """
        self.start_tour(
            "/web", "ssi_loan_loan_out_mark_principle_as_manual", login="admin"
        )

    def test_unmark_principle_as_manual(self):
        """Run the unmark principle as manual tour for ``loan.out``.

        IK: docs/loan_out/16-unmark-principle-as-manual.md
        """
        self.start_tour(
            "/web", "ssi_loan_loan_out_unmark_principle_as_manual", login="admin"
        )

    def test_realize_interest(self):
        """Run the realize interest tour for ``loan.out``.

        IK: docs/loan_out/17-realize-interest.md
        """
        self.start_tour("/web", "ssi_loan_loan_out_realize_interest", login="admin")

    def test_unrealize_interest(self):
        """Run the unrealize interest tour for ``loan.out``.

        IK: docs/loan_out/18-unrealize-interest.md
        """
        self.start_tour("/web", "ssi_loan_loan_out_unrealize_interest", login="admin")
