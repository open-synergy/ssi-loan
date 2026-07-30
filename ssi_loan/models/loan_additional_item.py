# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class LoanAdditionalItem(models.Model):
    """Master data for extra charges/fees billable on a loan schedule.

    Each record defines whether it applies to loan out and/or loan
    in (``loan_out_ok``/``loan_in_ok``) and the receivable/payable
    accounts and journals used to book it; selectable on
    ``loan.type.additional_item_ids`` and instantiated per schedule
    line as a ``loan.payment_schedule_*_additional_item``.
    """

    _name = "loan.additional_item"
    _inherit = ["mixin.master_data"]
    _description = "Loan Type"

    name = fields.Char(
        string="Loan Additional Item",
    )
    loan_out_ok = fields.Boolean(
        string="Available for Loan Out",
    )
    loan_in_ok = fields.Boolean(
        string="Available for Loan In",
    )
    receivable_account_id = fields.Many2one(
        string="Receivable Account",
        comodel_name="account.account",
    )
    contra_receivable_account_id = fields.Many2one(
        string="Contra-Receivable Account",
        comodel_name="account.account",
    )
    payable_account_id = fields.Many2one(
        string="Payable Account",
        comodel_name="account.account",
    )
    contra_payable_account_id = fields.Many2one(
        string="Contra-Payable Account",
        comodel_name="account.account",
    )
    receivable_journal_id = fields.Many2one(
        string="Receivable Journal",
        comodel_name="account.journal",
    )
    payable_journal_id = fields.Many2one(
        string="Payable Journal",
        comodel_name="account.journal",
    )
