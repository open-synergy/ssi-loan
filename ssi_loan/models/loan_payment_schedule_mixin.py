# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import UserError


class LoanPaymentScheduleMixin(models.AbstractModel):
    """Represent a single installment of a ``loan.mixin`` document.

    Tracks the principal, interest, and additional-item amounts due
    on ``schedule_date``, the reconciliation-derived payment state of
    each portion, and the accounting entries realizing the interest
    and additional items into the general ledger.
    """

    _name = "loan.payment_schedule_mixin"
    _description = "Loan Payment Schedule Mixin"

    @api.depends("principle_amount", "interest_amount", "additional_amount")
    def _compute_installment(self):
        """Sum principal, interest, and additional items per line.

        ``installment_amount`` is the total amount due for the
        schedule line.
        """
        for payment in self:
            payment.installment_amount = (
                payment.principle_amount
                + payment.interest_amount
                + payment.additional_amount
            )

    @api.depends("additional_item_ids", "additional_item_ids.amount")
    def _compute_additional_amount(self):
        """Sum the amounts of the schedule's additional items.

        Feeds ``installment_amount`` via ``_compute_installment``.
        """
        for record in self:
            result = 0.0
            for additional in record.additional_item_ids:
                result += additional.amount
            record.additional_amount = result

    @api.depends(
        "principle_move_line_id",
        "principle_move_line_id.matched_debit_ids",
        "principle_move_line_id.matched_credit_ids",
        "interest_move_line_id",
        "interest_move_line_id.matched_debit_ids",
        "interest_move_line_id.matched_credit_ids",
    )
    def _compute_state(self):
        """Derive payment states from move line reconciliation.

        ``principle_payment_state`` and ``interest_payment_state``
        are set to ``unpaid``, ``partial``, or ``paid`` depending on
        whether ``principle_move_line_id``/``interest_move_line_id``
        exist and are (partially) reconciled; interest starts as
        ``unrealized`` before its move line is created.
        """
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
        related="loan_id.currency_id",
        store=True,
    )
    schedule_date = fields.Date(
        string="Schedule Date",
        required=True,
        copy=False,
    )
    principle_amount = fields.Monetary(
        string="Principle Amount",
        required=True,
        copy=False,
        currency_field="currency_id",
    )
    interest_amount = fields.Monetary(
        string="Interest Amount",
        required=True,
        copy=False,
        currency_field="currency_id",
    )
    additional_amount = fields.Monetary(
        string="Additional Amount",
        compute="_compute_additional_amount",
        store=True,
        copy=False,
        compute_sudo=True,
        currency_field="currency_id",
    )
    installment_amount = fields.Monetary(
        string="Installment Amount",
        compute="_compute_installment",
        store=True,
        copy=False,
        compute_sudo=True,
        currency_field="currency_id",
    )
    principle_payment_state = fields.Selection(
        string="Principle Payment State",
        selection=[
            ("unpaid", "Unpaid"),
            ("partial", "Partial Paid"),
            ("paid", "Paid"),
            ("manual", "Manually Control"),
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
    additional_item_ids = fields.One2many(
        string="Additional Items",
        comodel_name="loan.payment_schedule_additional_item_mixin",
        inverse_name="schedule_id",
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

    def action_mark_principle_as_manual(self):
        """Switch the selected schedules to manual principal control.

        Delegates to ``_mark_principle_as_manual`` for each record
        run with ``sudo()``.
        """
        for record in self.sudo():
            record._mark_principle_as_manual()

    def action_unmark_principle_as_manual(self):
        """Revert the selected schedules to automatic principal.

        Delegates to ``_unmark_principle_as_manual`` for each record
        run with ``sudo()``.
        """
        for record in self.sudo():
            record._unmark_principle_as_manual()

    def action_realize_interest(self):
        """Post interest and additional-item entries for schedules.

        Delegates to ``_create_interest_realization_move`` and
        ``_create_additional_item_move`` for each record run with
        ``sudo()``.
        """
        for schedule in self.sudo():
            schedule._create_interest_realization_move()
            schedule._create_additional_item_move()

    def action_unrealize_interest(self):
        """Reverse interest and additional-item entries for schedules.

        Delegates to ``_delete_interest_realization_move`` and
        ``_delete_additional_item_move`` for each record run with
        ``sudo()``.
        """
        for schedule in self.sudo():
            schedule._delete_interest_realization_move()
            schedule._delete_additional_item_move()

    def _mark_principle_as_manual(self):
        """Set ``principle_payment_state`` to ``manual``.

        Once manual, the schedule's principal is excluded from
        ``loan.total_principle_amount`` and tracked separately.
        """
        self.ensure_one()
        self.write(
            {
                "principle_payment_state": "manual",
            }
        )

    def _unmark_principle_as_manual(self):
        """Reset ``principle_payment_state`` back to ``unpaid``."""
        self.ensure_one()
        self.write(
            {
                "principle_payment_state": "unpaid",
            }
        )

    def _create_additional_item_move(self):
        """Post the accounting entry for every additional item.

        Delegates to ``action_create_accounting_entry`` on each
        record in ``additional_item_ids``.
        """
        self.ensure_one()
        for additional_item in self.additional_item_ids:
            additional_item.action_create_accounting_entry()

    def _delete_additional_item_move(self):
        """Reverse the accounting entry for every additional item.

        Delegates to ``action_delete_accounting_entry`` on each
        record in ``additional_item_ids``.
        """
        self.ensure_one()
        for additional_item in self.additional_item_ids:
            additional_item.action_delete_accounting_entry()

    def _delete_interest_realization_move(self):
        """Delete the schedule's interest realization journal entry."""
        self.ensure_one()
        self.interest_move_id.with_context(force_delete=True).unlink()

    def _prepare_interest_realization_move(self):
        """Build the ``account.move`` header for interest realization.

        Extension point: override to change the journal, date, or
        reference used for the interest entry.

        :return: dict of ``account.move`` values
        """
        self.ensure_one()
        loan = self.loan_id
        res = {
            "name": "/",
            "journal_id": self._get_interest_journal().id,
            "date": self.schedule_date,
            "ref": loan.name,
            "currency_id": self.currency_id.id,
        }
        return res

    def _get_interest_journal(self):
        """Resolve the journal used for the interest entry.

        Extension point: override to source the journal from
        elsewhere than ``loan_id.type_id.interest_journal_id``.

        :return: an ``account.journal`` record
        :raises UserError: if the loan type has no interest journal
            defined
        """
        self.ensure_one()
        loan = self.loan_id
        journal = loan.type_id.interest_journal_id

        if not journal:
            msg = _("No interest journal defined")
            raise UserError(msg)

        return journal

    def _create_interest_realization_move(self):
        """Post the interest realization journal entry.

        Creates the ``account.move``, the interest receivable line
        (stored on ``interest_move_line_id``), and the interest
        income line, then posts the move.
        """
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

        move.action_post()

    def _prepare_interest_realization_move_line(self, move):
        """Build the interest receivable ``account.move.line`` values.

        Extension point: override to change the account or partner
        used for the interest receivable line.

        :param move: the ``account.move`` the line will belong to
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        loan = self.loan_id
        loan_type = loan.type_id
        name = _("%s %s interest receivable") % (loan.name, self.schedule_date)

        (
            debit,
            credit,
            amount_currency,
        ) = self._get_interest_realization_move_line_amount()

        res = {
            "move_id": move.id,
            "name": name,
            "account_id": loan_type.account_interest_id.id,
            "debit": debit,
            "credit": credit,
            "date_maturity": self.schedule_date,
            "partner_id": loan.partner_id.id,
            "currency_id": self.currency_id.id,
            "amount_currency": amount_currency,
        }
        return res

    def _get_interest_realization_move_line_amount(self):
        """Compute the interest receivable debit/credit amounts.

        Converts ``interest_amount`` to the loan's company currency
        and splits it between debit and credit based on
        ``loan_id.direction``.

        Extension point: override to change how the interest
        receivable amount is booked.

        :return: tuple of ``(debit, credit, amount_currency)``
        """
        self.ensure_one()
        debit = credit = 0.0
        loan = self.loan_id
        interest_amount = self.currency_id._convert(
            from_amount=self.interest_amount,
            to_currency=loan.company_currency_id,
            company=loan.company_id,
            date=self.schedule_date,
        )

        if loan.direction == "in":
            credit = interest_amount
            amount_currency = -1.0 * self.interest_amount
        else:
            debit = interest_amount
            amount_currency = self.interest_amount
        return debit, credit, amount_currency

    def _prepare_interest_income_move_line(self, move):
        """Build the interest income ``account.move.line`` values.

        Extension point: override to change the account or partner
        used for the interest income line.

        :param move: the ``account.move`` the line will belong to
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        loan = self.loan_id
        name = _("%s %s interest income") % (loan.name, self.schedule_date)
        debit, credit, amount_currency = self._get_interest_move_line_amount()
        res = {
            "move_id": move.id,
            "name": name,
            "account_id": self._get_interest_income_account().id,
            "credit": credit,
            "debit": debit,
            "date_maturity": self.schedule_date,
            "partner_id": self.loan_id.partner_id.id,
            "currency_id": self.currency_id.id,
            "amount_currency": amount_currency,
        }
        return res

    def _get_interest_move_line_amount(self):
        """Compute the interest income debit/credit amounts.

        Converts ``interest_amount`` to the loan's company currency
        and splits it between debit and credit based on
        ``loan_id.direction`` (mirrored versus the receivable line).

        Extension point: override to change how the interest income
        amount is booked.

        :return: tuple of ``(debit, credit, amount_currency)``
        """
        self.ensure_one()
        debit = credit = 0.0
        loan = self.loan_id
        interest_amount = self.currency_id._convert(
            from_amount=self.interest_amount,
            to_currency=loan.company_currency_id,
            company=loan.company_id,
            date=self.schedule_date,
        )

        if loan.direction == "out":
            credit = interest_amount
            amount_currency = -1.0 * self.interest_amount
        else:
            debit = interest_amount
            amount_currency = self.interest_amount
        return debit, credit, amount_currency

    def _get_interest_income_account(self):
        """Resolve the account used for the interest income line.

        Extension point: override to source the account from
        elsewhere than ``loan_id.type_id.account_interest_income_id``.

        :return: an ``account.account`` record
        :raises UserError: if the loan type has no interest income
            account defined
        """
        self.ensure_one()
        loan = self.loan_id
        account = loan.type_id.account_interest_income_id

        if not account:
            msg = _("No interest income account defined")
            raise UserError(msg)

        return account

    def _create_principle_receivable_move_line(self, move):
        """Post the principal receivable line onto the given move.

        Stores the created line on ``principle_move_line_id``.

        :param move: the ``account.move`` the line will belong to
        """
        self.ensure_one()
        line = (
            self.env["account.move.line"]
            .with_context(check_move_validity=False)
            .create(self._prepare_principle_receivable_move_line(move))
        )
        self.principle_move_line_id = line

    def _prepare_principle_receivable_move_line(self, move):
        """Build the principal receivable ``account.move.line`` values.

        Extension point: override to change the account or partner
        used for the principal receivable line.

        :param move: the ``account.move`` the line will belong to
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        loan = self.loan_id
        name = _("%s %s principle receivable") % (loan.name, self.schedule_date)
        debit, credit, amount_currency = self._get_realization_move_line_amount()
        account = self._get_realization_move_line_account()
        res = {
            "move_id": move.id,
            "name": name,
            "account_id": account.id,
            "debit": debit,
            "credit": credit,
            "date_maturity": self.schedule_date,
            "partner_id": loan.partner_id.id,
            "currency_id": self.currency_id.id,
            "amount_currency": amount_currency,
        }
        return res

    def _get_realization_move_line_amount(self):
        """Compute the principal receivable debit/credit amounts.

        Converts ``principle_amount`` to the loan's company currency
        and splits it between debit and credit based on
        ``loan_id.direction``.

        Extension point: override to change how the principal amount
        is booked.

        :return: tuple of ``(debit, credit, amount_currency)``
        """
        self.ensure_one()
        loan = self.loan_id
        debit = credit = amount_currency = 0.0

        principle_amount = loan._convert_amount_to_company_currency(
            self.principle_amount
        )

        if loan.direction == "in":
            credit = principle_amount
            amount_currency = self.principle_amount * -1.0
        else:
            debit = principle_amount
            amount_currency = self.principle_amount

        return debit, credit, amount_currency

    def _get_realization_move_line_account(self):
        """Resolve the principal account for the receivable line.

        Extension point: override to change the long/short-term
        account selection rule (currently based on whether
        ``schedule_date`` is more than 365 days from today).

        :return: an ``account.account`` record
        :raises UserError: if the loan type has no matching
            long-term or short-term principal account defined
        """
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
