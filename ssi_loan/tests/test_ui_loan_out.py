# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiLoanOut(HttpCase):
    """Tour tests for the ``loan.out`` work instructions."""

    @classmethod
    def setUpClass(cls):
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
        """
        super().setUpClass()
        cls.env.ref("base.USD").sudo().write({"active": True})
        cls.env.ref("base.user_admin").sudo().write(
            {"groups_id": [(4, cls.env.ref("ssi_loan.loan_out_validator_group").id)]}
        )

        receivable_type = cls.env.ref("account.data_account_type_receivable")
        revenue_type = cls.env.ref("account.data_account_type_revenue")
        account_realization = cls.env["account.account"].create(
            {
                "code": "TOURLO01",
                "name": "Tour Loan Out Realization Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_rounding = cls.env["account.account"].create(
            {
                "code": "TOURLO02",
                "name": "Tour Loan Out Rounding Account",
                "user_type_id": revenue_type.id,
            }
        )
        account_interest = cls.env["account.account"].create(
            {
                "code": "TOURLO03",
                "name": "Tour Loan Out Interest Account",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        account_interest_income = cls.env["account.account"].create(
            {
                "code": "TOURLO04",
                "name": "Tour Loan Out Interest Income Account",
                "user_type_id": revenue_type.id,
            }
        )
        realization_journal = cls.env["account.journal"].create(
            {
                "name": "Tour Loan Out Realization Journal",
                "code": "TLOJ1",
                "type": "general",
            }
        )
        interest_journal = cls.env["account.journal"].create(
            {
                "name": "Tour Loan Out Interest Journal",
                "code": "TLOJ2",
                "type": "general",
            }
        )
        cls.loan_type = cls.env["loan.type"].create(
            {
                "name": "Tour Loan Type Out",
                "code": "/",
                "direction": "out",
                "interest_method": "flat",
                "currency_id": cls.env.ref("base.USD").id,
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
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "Tour Cancel Reason",
                "code": "TOURX01",
                "global_use": True,
            }
        )

        # Pre-Condition IK 14-compute-payment-schedule.md: draft record
        # with Loan Type/Amount/Interest/Period/First Payment Date
        # already filled, schedule NOT computed yet.
        partner_schedule = cls.env["res.partner"].create(
            {"name": "Tour Loan Out Schedule Partner"}
        )
        cls.loan_out_schedule = cls.env["loan.out"].create(
            cls._loan_out_values(partner_schedule)
        )

        # Pre-Condition IK 04-confirm.md: draft record whose Total
        # Principle Amount already equals Loan Amount.
        partner_confirm = cls.env["res.partner"].create(
            {"name": "Tour Loan Out Confirm Partner"}
        )
        cls.loan_out_confirm = cls.env["loan.out"].create(
            cls._loan_out_values(partner_confirm)
        )
        cls.loan_out_confirm.action_compute_payment()

        # Pre-Condition IK 05-approve.md: record already Waiting for
        # Approval, with ``admin`` as its active approver.
        partner_approve = cls.env["res.partner"].create(
            {"name": "Tour Loan Out Approve Partner"}
        )
        cls.loan_out_approve = cls.env["loan.out"].create(
            cls._loan_out_values(partner_approve)
        )
        cls.loan_out_approve.action_compute_payment()
        cls.loan_out_approve.with_context(bypass_policy_check=True).action_confirm()

        # Pre-Condition IK 10-cancel.md: a plain Draft record (cancel is
        # also allowed from Draft, so no schedule/confirm needed).
        partner_cancel = cls.env["res.partner"].create(
            {"name": "Tour Loan Out Cancel Partner"}
        )
        cls.loan_out_cancel = cls.env["loan.out"].create(
            cls._loan_out_values(partner_cancel)
        )

    @classmethod
    def _loan_out_values(cls, partner):
        """Build ``loan.out`` create values shared by the fixtures.

        :param partner: ``res.partner`` record to use as borrower
        :return: dict of field values for ``loan.out.create``
        """
        return {
            "date": "2024-01-01",
            "partner_id": partner.id,
            "type_id": cls.loan_type.id,
            "currency_id": cls.env.ref("base.USD").id,
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
