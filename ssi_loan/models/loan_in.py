# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LoanIn(models.Model):
    """Represent a loan the company receives from a third party.

    Restricts ``type_id`` to incoming loan types and routes payment
    schedules and collateral to their ``*.in`` counterparts; the
    borrowing/payable lifecycle itself is inherited from
    ``loan.mixin``.
    """

    _name = "loan.in"
    _inherit = ["loan.mixin"]
    _description = "Loan In"

    type_id = fields.Many2one(
        domain=[
            ("direction", "=", "in"),
        ],
    )
    direction = fields.Selection(
        related="type_id.direction",
        store=True,
    )
    payment_schedule_ids = fields.One2many(
        comodel_name="loan.payment_schedule_in",
    )
    collateral_ids = fields.One2many(
        comodel_name="loan_in.collateral",
    )
