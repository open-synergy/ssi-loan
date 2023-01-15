# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class LoanCollateralOut(models.Model):
    _name = "loan_out.collateral"
    _inherit = ["loan.collateral_mixin"]
    _description = "Loan Collateral Out"

    loan_id = fields.Many2one(
        comodel_name="loan.out",
    )
