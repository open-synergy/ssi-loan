# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class LoanPaymentScheduleInAdditionalItem(models.Model):
    """Extra charge/fee line attached to a ``loan.payment_schedule_in``.

    Detail model of ``loan.payment_schedule_in``: adds the
    ``schedule_id`` back-reference and the journal/payable accounts
    used to book the item, on top of the amount and
    ``additional_item_id`` reference inherited from
    ``loan.payment_schedule_additional_item_mixin``.
    """

    _name = "loan.payment_schedule_in_additional_item"
    _inherit = "loan.payment_schedule_additional_item_mixin"
    _description = "Loan Payment Schedule In Additional Item"

    schedule_id = fields.Many2one(
        comodel_name="loan.payment_schedule_in",
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
    )
    reconcilliation_account_id = fields.Many2one(
        string="Payable Account",
    )
    contra_reconcilliation_account_id = fields.Many2one(
        string="Contra-Payable Account",
    )
