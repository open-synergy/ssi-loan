# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class LoanIn(models.Model):
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
