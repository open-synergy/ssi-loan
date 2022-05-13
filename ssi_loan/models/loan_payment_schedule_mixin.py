# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import _, api, fields, models
from odoo.exceptions import UserError


class LoanPaymentScheduleMixin(models.AbstractModel):
    _name = "loan.payment_schedule_mixin"
    _description = "Loan Payment Schedule Mixin"

    @api.depends("principle_amount", "interest_amount")
    def _compute_installment(self):
        for payment in self:
            payment.installment_amount = (
                payment.principle_amount + payment.interest_amount
            )

    @api.depends(
        "principle_move_line_id",
        "principle_move_line_id.matched_debit_ids",
        "principle_move_line_id.matched_credit_ids",
        "interest_move_line_id",
        "interest_move_line_id.matched_debit_ids",
        "interest_move_line_id.matched_credit_ids",
    )
    def _compute_state(self):
        for payment in self:
            principle_move_line = payment.principle_move_line_id
            interest_move_line = payment.interest_move_line_id

            if not principle_move_line:
                payment.principle_payment_state = "unpaid"
            elif (
                not principle_move_line.reconciled
                and not principle_move_line.matched_debit_ids
                and not principle_move_line.matched_credit_ids
            ):
                payment.principle_payment_state = "unpaid"
            elif not principle_move_line.reconciled:
                payment.principle_payment_state = "partial"
            elif principle_move_line.reconciled:
                payment.principle_payment_state = "paid"

            if not interest_move_line:
                payment.interest_payment_state = "unrealized"
            elif (
                not interest_move_line.reconciled
                and not interest_move_line.matched_debit_ids
                and not interest_move_line.matched_credit_ids
            ):
                payment.interest_payment_state = "unpaid"
            elif not interest_move_line.reconciled:
                payment.interest_payment_state = "partial"
            elif interest_move_line.reconciled:
                payment.interest_payment_state = "paid"

    loan_id = fields.Many2one(
        string="# Loan",
        comodel_name="loan.mixin",
        ondelete="cascade",
        copy=False,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        readonly=True,
        copy=False,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        readonly=True,
        copy=False,
    )
    schedule_date = fields.Date(
        string="Schedule Date",
        required=True,
        copy=False,
    )
    principle_amount = fields.Float(
        string="Principle Amount",
        required=True,
        copy=False,
    )
    interest_amount = fields.Float(
        string="Interest Amount",
        required=True,
        copy=False,
    )
    installment_amount = fields.Float(
        string="Installment Amount",
        compute="_compute_installment",
        store=True,
        copy=False,
        compute_sudo=True,
    )
    principle_payment_state = fields.Selection(
        string="Principle Payment State",
        selection=[
            ("unpaid", "Unpaid"),
            ("partial", "Partial Paid"),
            ("paid", "Paid"),
        ],
        compute="_compute_state",
        store=True,
        copy=False,
        compute_sudo=True,
    )
    interest_payment_state = fields.Selection(
        string="Interest Payment State",
        selection=[
            ("unrealized", "Unrealized"),
            ("unpaid", "Unpaid"),
            ("partial", "Partial Paid"),
            ("paid", "Paid"),
        ],
        compute="_compute_state",
        store=True,
        copy=False,
        compute_sudo=True,
    )
    principle_move_line_id = fields.Many2one(
        string="Principle Move Line",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
    )
    old_principle_move_line_id = fields.Many2one(
        string="Old Principle Move Line",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
    )
    principle_move_id = fields.Many2one(
        string="Principle Move",
        comodel_name="account.move",
        copy=False,
    )
    interest_move_line_id = fields.Many2one(
        string="Interest Move Line",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
    )
    interest_move_id = fields.Many2one(
        string="Interest Move",
        comodel_name="account.move",
        copy=False,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Waiting for Realization"),
            ("active", "Active"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        readonly=True,
        copy=False,
    )

    def action_realize_interest(self):
        for schedule in self.sudo():
            schedule._create_interest_realization_move()

    def action_unrealize_interest(self):
        for schedule in self.sudo():
            schedule._delete_interest_realization_move()

    def _delete_interest_realization_move(self):
        self.ensure_one()
        self.interest_move_id.with_context(force_delete=True).unlink()

    def _prepare_interest_realization_move(self):
        self.ensure_one()
        loan = self.loan_id
        res = {
            "name": "/",
            "journal_id": self._get_interest_journal().id,
            "date": self.schedule_date,
            "ref": loan.name,
        }
        return res

    def _get_interest_journal(self):
        self.ensure_one()
        loan = self.loan_id
        journal = loan.type_id.interest_journal_id

        if not journal:
            msg = _("No interest journal defined")
            raise UserError(msg)

        return journal

    def _create_interest_realization_move(self):
        self.ensure_one()
        obj_move = self.env["account.move"]
        obj_line = self.env["account.move.line"]

        move = obj_move.create(self._prepare_interest_realization_move())

        line_receivable = obj_line.with_context(check_move_validity=False).create(
            self._prepare_interest_realization_move_line(move)
        )

        self.interest_move_line_id = line_receivable

        obj_line.with_context(check_move_validity=False).create(
            self._prepare_interest_income_move_line(move)
        )

    def _prepare_interest_realization_move_line(self, move):
        self.ensure_one()
        loan = self.loan_id
        loan_type = loan.type_id
        name = _("%s %s interest receivable") % (loan.name, self.schedule_date)

        debit, credit = self._get_interest_realization_move_line_amount()

        res = {
            "move_id": move.id,
            "name": name,
            "account_id": loan_type.account_interest_id.id,
            "debit": debit,
            "credit": credit,
            "date_maturity": self.schedule_date,
            "partner_id": loan.partner_id.id,
        }
        return res

    def _get_interest_realization_move_line_amount(self):
        self.ensure_one()
        debit = credit = 0.0
        loan = self.loan_id
        if loan.direction == "in":
            credit = self.interest_amount
        else:
            debit = self.interest_amount
        return debit, credit

    def _prepare_interest_income_move_line(self, move):
        self.ensure_one()
        loan = self.loan_id
        name = _("%s %s interest income") % (loan.name, self.schedule_date)
        debit, credit = self._get_interest_move_line_amount()
        res = {
            "move_id": move.id,
            "name": name,
            "account_id": self._get_interest_income_account().id,
            "credit": credit,
            "debit": debit,
            "date_maturity": self.schedule_date,
            "partner_id": self.loan_id.partner_id.id,
        }
        return res

    def _get_interest_move_line_amount(self):
        self.ensure_one()
        debit = credit = 0.0
        loan = self.loan_id
        if loan.direction == "out":
            credit = self.interest_amount
        else:
            debit = self.interest_amount
        return debit, credit

    def _get_interest_income_account(self):
        self.ensure_one()
        loan = self.loan_id
        account = loan.type_id.account_interest_income_id

        if not account:
            msg = _("No interest income account defined")
            raise UserError(msg)

        return account

    def _create_principle_receivable_move_line(self, move):
        self.ensure_one()
        line = (
            self.env["account.move.line"]
            .with_context(check_move_validity=False)
            .create(self._prepare_principle_receivable_move_line(move))
        )
        self.principle_move_line_id = line

    def _prepare_principle_receivable_move_line(self, move):
        self.ensure_one()
        loan = self.loan_id
        name = _("%s %s principle receivable") % (loan.name, self.schedule_date)
        debit, credit = self._get_realization_move_line_amount()
        account = self._get_realization_move_line_account()
        res = {
            "move_id": move.id,
            "name": name,
            "account_id": account.id,
            "debit": debit,
            "credit": credit,
            "date_maturity": self.schedule_date,
            "partner_id": loan.partner_id.id,
        }
        return res

    def _get_realization_move_line_amount(self):
        self.ensure_one()
        debit = credit = 0.0
        loan = self.loan_id
        if loan.direction == "in":
            credit = self.principle_amount
        else:
            debit = self.principle_amount
        return debit, credit

    def _get_realization_move_line_account(self):
        self.ensure_one()
        dt_today = fields.Date.today()
        loan = self.loan_id
        dt_schedule = fields.Date.to_date(self.schedule_date)
        account = False
        if abs((dt_schedule - dt_today).days) > 365:
            account = loan.type_id.long_account_principle_id
            if not account:
                msg = _("No long-term principle account defined")
                raise UserError(msg)
        else:
            account = loan.type_id.short_account_principle_id
            if not account:
                msg = _("No short-term principle account defined")
                raise UserError(msg)
        return account
