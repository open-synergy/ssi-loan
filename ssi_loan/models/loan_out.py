# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LoanOut(models.Model):
    """Represent a loan disbursed by the company to a third party.

    Restricts ``type_id`` to outgoing loan types and routes payment
    schedules and collateral to their ``*.out`` counterparts; the
    disbursement/receivable lifecycle itself is inherited from
    ``loan.mixin``.
    """

    _name = "loan.out"
    _inherit = ["loan.mixin"]
    _description = "Loan Out"

    type_id = fields.Many2one(
        domain=[
            ("direction", "=", "out"),
        ],
    )
    direction = fields.Selection(
        related="type_id.direction",
        store=True,
    )
    payment_schedule_ids = fields.One2many(
        comodel_name="loan.payment_schedule_out",
    )
    collateral_ids = fields.One2many(
        comodel_name="loan_out.collateral",
    )
